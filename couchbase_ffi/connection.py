from warnings import warn, warn_explicit

from couchbase.transcoder import TranscoderPP
from couchbase.connection import Connection as _ExtConnection
from couchbase.user_constants import *
from couchbase.exceptions import (
    CouchbaseError,
    ValueFormatError,
    ArgumentError,
    HTTPError
)
from couchbase._libcouchbase import PYCBC_CONN_F_WARNEXPLICIT

from couchbase_ffi._cinit import get_handle, CALLBACK_DECLS
from couchbase_ffi.result import (
    MultiResult,
    OperationResult,
    ValueResult,
    ObserveInfo,
    HttpResult
)

from couchbase_ffi.context import (
    CommandContext,
    GetCommandContext,
    LockCommandContext,
    StoreCommandContext,
    RemoveCommandContext,
    IncrCommandContext,
    DecrCommandContext,
    TouchCommandContext,
    UnlockCommandContext,
    ObserveCommandContext,
    StatsCommandContext,
    Options
)

import couchbase_ffi.context

ffi, C = get_handle()

couchbase_ffi.context.ffi = ffi
couchbase_ffi.context.C = C

def gen_mutator_pair(mode):
    def _m_single(self, key, value, **kwargs):
        try:
            kv = { key: value }
        except Exception as e:
            raise ValueFormatError.pyexc("Unhashable key", obj=key, inner=e)

        ctx = StoreCommandContext(self, mode, kv, **kwargs)
        return self._invoke_common(C.lcb_store, ctx, False)

    def _m_multi(self, kv, **kwargs):
        if 'cas' in kwargs:
            raise ArgumentError.pyexc("CAS cannot be supplied to a "
                                      "multi operation")
        ctx = StoreCommandContext(self, mode, kv, **kwargs)
        return self._invoke_common(C.lcb_store, ctx, True)

    return (_m_single, _m_multi)

def gen_mutators():
    mnames = (
        ('set', C.LCB_SET),
        ('add', C.LCB_ADD),
        ('replace', C.LCB_REPLACE),
        ('append', C.LCB_APPEND),
        ('prepend', C.LCB_PREPEND))

    d = {}

    for mutator, mode in mnames:
        m_single, m_multi = gen_mutator_pair(mode)
        d[mutator] = m_single
        d[mutator+"_multi"] = m_multi

    return d


def gen_simple_pair(ctxcls, fn):
    def _m_single(self, key, *args, **kwargs):
        kwargs['posargs'] = args
        ctx = ctxcls(self, (key,), **kwargs)
        return self._invoke_common(fn, ctx, False)

    def _m_multi(self, kv, **kwargs):
        if 'cas' in kwargs:
            raise ArgumentError.pyexc("CAS cannot be an argument to a "
                                      "multi operation")
        ctx = ctxcls(self, kv, **kwargs)
        return self._invoke_common(fn, ctx, True)

    return (_m_single, _m_multi)

def gen_simple():
    mnames = (
        ('get', GetCommandContext, C.lcb_get),
        ('lock', LockCommandContext, C.lcb_get),
        ('incr', IncrCommandContext, C.lcb_arithmetic),
        ('decr', DecrCommandContext, C.lcb_arithmetic),
        ('delete', RemoveCommandContext, C.lcb_remove),
        ('unlock', UnlockCommandContext, C.lcb_unlock),
        ('touch', TouchCommandContext, C.lcb_touch),
        ('observe', ObserveCommandContext, C.lcb_observe)
    )

    d = {}

    for name, ctxcls, lcbfunc in mnames:
        m_single, m_multi = gen_simple_pair(ctxcls, lcbfunc)
        d[name] = m_single
        d[name + "_multi"] = m_multi

    return d


class OperationInfo(object):
    __slots__ = ('exc', 'ctx', 'res')

    def __init__(self):
        self.start(None)

    def start(self, ctx):
        self.exc = None
        self.ctx = ctx
        self.res = MultiResult()

    def throw(self, exc):
        self.res.all_ok = False
        if self.exc:
            return

        self.exc = exc
        self.exc.all_results = self.res

    def rethrow(self):
        if self.exc:
            raise self.exc


    def _warn_dup_key(self, key, conn):
        msg = "Duplicate key {0} found".format(key)
        if conn._privflags & PYCBC_CONN_F_WARNEXPLICIT:
            warn_explicit(msg,
                          RuntimeWarning,
                          __file__, -1,
                          module="couchbase_ffi.connection",
                          registry={})
        else:
            warn(msg, RuntimeWarning)

    def add_single(self, pres, key, conn):
        pres.key = key
        try:
            if key in self.res:
                self._warn_dup_key(key, conn)

            self.res[key] = pres

        except TypeError as e:
            self.throw(ValueFormatError.pyexc("Unhashable key", obj=key))
            return

        self.update_single(pres, conn)

    def update_single(self, pres, conn):
        if not pres.rc:
            return

        self.res.all_ok = False
        if pres.rc == C.LCB_KEY_ENOENT and self.ctx.quiet or conn.quiet:
            return

        self.throw(conn._make_exc(pres.rc, pres))

    def mkret(self, is_multi):
        if is_multi:
            return self.res
        return self.res.values()[0]

class ShadowProperties(object):
    MEMBER_NAME = '_shadow_props_instance_dict'
    def __init__(self):
        self._d = {}

    def _gen_prop(sp_self, name, verify_set=None):
        def x_get(self):
            return getattr(self, sp_self.MEMBER_NAME)[name]

        def x_set(self, val):
            if verify_set:
                val = verify_set(val)

            getattr(_ExtConnection, name).__set__(self, val)
            getattr(self, sp_self.MEMBER_NAME)[name] = val

        return property(x_get, x_set)

    def add(self, name, set_xfrm=None):
        self._d[name] = self._gen_prop(name, set_xfrm)

    def init_instance_vars(self_clsvar, instance):
        d = getattr(instance, self_clsvar.MEMBER_NAME)
        for name in self_clsvar._d:
            d[name] = getattr(_ExtConnection, name).__get__(instance)

    def get_name_dict(self):
        return self._d


class pycbc_cpy(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, fn):
        def wrap(self, *args, **kwargs):
            if not self.expose_extension_methods:
                raise NotImplementedError("Method not available for FFI")
            else:
                return getattr(_ExtConnection, name)(self, *args, **kwargs)

        return wrap

def _verify_transcoder(tc):
    if not tc:
        tc = TranscoderPP()

    return tc

class Connection(_ExtConnection):
    _shadow_props_cls = ShadowProperties()
    _shadow_props_cls.add('quiet')
    _shadow_props_cls.add('default_format')
    _shadow_props_cls.add('transcoder', _verify_transcoder)
    _shadow_props_cls.add('data_passthrough')
    locals().update(_shadow_props_cls.get_name_dict())

    @property
    def _tc(self):
        return self.transcoder

    def _init_instance(self):
        C.lcb_set_store_callback(self._instance, self._bound_cb['store'])
        C.lcb_set_get_callback(self._instance, self._bound_cb['get'])
        C.lcb_set_remove_callback(self._instance, self._bound_cb['remove'])
        C.lcb_set_arithmetic_callback(self._instance, self._bound_cb['arith'])
        C.lcb_set_touch_callback(self._instance, self._bound_cb['touch'])
        C.lcb_set_unlock_callback(self._instance, self._bound_cb['unlock'])
        C.lcb_set_error_callback(self._instance, self._bound_cb['error'])
        C.lcb_set_stat_callback(self._instance, self._bound_cb['stats'])
        C.lcb_set_observe_callback(self._instance, self._bound_cb['observe'])
        C.lcb_set_http_complete_callback(self._instance, self._bound_cb['htdone'])

    def __init__(self, **kwargs):
        kwargs['unlock_gil'] = False
        kwargs['lockmode'] = LOCKMODE_NONE
        setattr(self, self._shadow_props_cls.MEMBER_NAME, {})
        super(Connection, self).__init__(**kwargs)

        # Load the instance variables from the base
        self._shadow_props_cls.init_instance_vars(self)

        self._instance = ffi.cast('lcb_t', self._instance_pointer)

        self._bound_cb = {
            'store': ffi.callback(CALLBACK_DECLS['store'],
                                  self._storage_callback),
            'get': ffi.callback(CALLBACK_DECLS['get'],
                                self._get_callback),
            'remove': ffi.callback(CALLBACK_DECLS['delete'],
                                   self._opres_callback),
            'arith': ffi.callback(CALLBACK_DECLS['arith'],
                                  self._arith_callback),
            'error': ffi.callback(CALLBACK_DECLS['error'],
                                  self._error_callback),
            'touch': ffi.callback(CALLBACK_DECLS['touch'],
                                  self._opres_callback),
            'unlock': ffi.callback(CALLBACK_DECLS['unlock'],
                                   self._unlock_callback),
            'stats': ffi.callback(CALLBACK_DECLS['stats'],
                                  self._stats_callback),
            'observe': ffi.callback(CALLBACK_DECLS['observe'],
                                    self._observe_callback),
            'htdone': ffi.callback(CALLBACK_DECLS['http'],
                                   self._http_complete_callback)
        }

        self._cur = OperationInfo()
        self.transcoder = TranscoderPP()
        self._init_instance()
        self.expose_extension_methods = kwargs.get('expose_extension_methods',
                                                   False)

    # Reimplement
    def _close(self):
        super(Connection, self)._close()
        self._instance = ffi.cast('lcb_t', self._instance_pointer)
        self._init_instance()

    @pycbc_cpy('pipeline')
    def pipeline(self): pass

    @pycbc_cpy('durability')
    def durability(self, *args, **kwargs): pass

    @pycbc_cpy('endure')
    def endure(self, *args, **kwargs): pass

    @pycbc_cpy('endure_multi')
    def endure_multi(self, *args, **kwargs): pass

    @pycbc_cpy('rget')
    def rget(self, *args, **kwargs): pass

    @pycbc_cpy('rget_multi')
    def rget_multi(self, *args, **kwargs): pass

    def _stats(self, keys):
        ctx = StatsCommandContext(self, keys)
        return self._invoke_common(C.lcb_server_stats, ctx, True)

    def _get_response_key(self, resp):
        key = ffi.buffer(resp.v.v0.key, resp.v.v0.nkey)[:]
        key = self._tc.decode_key(key)
        return key

    def _add_response(self, cres, pres):
        try:
            key = self._get_response_key(cres)

        except Exception as e:
            self._cur.throw(e)
            return

        self._cur.add_single(pres, key, self)

    def _get_response(self, cres, err, cls):
        """
        Used for multi-key callbacks like stats and observe
        """
        try:
            key = self._get_response_key(cres)
        except Exception as e:
            self._cur.throw(e)
            return None


        res = self._cur.res.get(key, None)
        is_new = False
        if res is None:
            res = cls()
            is_new = True

        res.rc = err
        if is_new:
            self._add_response(cres, res)
        else:
            self._cur.update_single(res, self)

        return res

    def _unlock_callback(self, instance, cookie, err, resp):
        res = OperationResult()
        res.rc = err
        self._add_response(resp, res)

    def _opres_callback(self, instance, cookie, err, resp):
        res = OperationResult()
        res.cas = resp.v.v0.cas
        res.rc = err
        self._add_response(resp, res)

    def _storage_callback(self, instance, cookie, op, err, resp):
        self._opres_callback(instance, cookie, err, resp)

    def _get_callback(self, instance, cookie, err, resp):
        res = ValueResult()
        res.cas = resp.v.v0.cas
        res.flags = resp.v.v0.flags
        res.rc = err

        if not err:
            value = ffi.buffer(resp.v.v0.bytes, resp.v.v0.nbytes)[:]
            effective_format = resp.v.v0.flags
            if self.data_passthrough or self._cur.ctx.no_format:
                effective_format = FMT_BYTES

            try:
                value = self._tc.decode_value(value, effective_format)
                res.value = value

            except Exception as e:
                res.value = None
                exc = ValueFormatError.pyexc(inner=e, obj=value)
                self._cur.throw(exc)

        else:
            res.value = None

        self._add_response(resp, res)

    def _arith_callback(self, instance, cookie, err, resp):
        res = ValueResult()
        res.cas = resp.v.v0.cas
        res.value = resp.v.v0.value
        res.rc = err
        self._add_response(resp, res)

    def _error_callback(self, instance, errcode, errmsg):
        t = (errcode, ffi.string(errmsg) if errmsg else "")
        self._errors.append(t)

    def _observe_callback(self, instance, cookie, err, resp):
        # Special handling needed here, as this is a multi operation
        if not resp.v.v0.key:
            return #NULL

        res = self._get_response(resp, err, ValueResult)
        if not res:
            # Error
            return

        obs_l = res.value
        if obs_l is None:
            res.value = []
            obs_l = res.value

        obs_info = ObserveInfo()
        obs_info.cas = resp.v.v0.cas
        obs_info.flags = resp.v.v0.status
        obs_info.from_master = bool(resp.v.v0.from_master)
        obs_l.append(obs_info)

    def _stats_callback(self, instance, cookie, err, resp):
        if not resp.v.v0.server_endpoint:
            return # Done
        if err:
            self._cur.throw(self._make_exc(err))
            return

        key = ffi.buffer(resp.v.v0.key, resp.v.v0.nkey)[:]
        val = ffi.buffer(resp.v.v0.bytes, resp.v.v0.nbytes)[:]

        try:
            val = float(val)
        except:
            pass

        server = ffi.string(resp.v.v0.server_endpoint)

        res = self._cur.res
        d = self._cur.res.setdefault(key, {})
        d[server] = val

    def _endure_callback(self, instance, cookie, err, resp):
        if err == C.LCB_SUCCESS:
            err = resp.v.v0.err

        res = self._get_response(resp, err, OperationResult)
        if not res:
            return

        # Not very exciting, is it.. eh?

    def _make_exc(self, rc, res=None):
        cls = CouchbaseError.rc_to_exctype(rc)
        exc = cls("")
        exc.rc = rc
        exc.all_results = self._cur.res
        exc.message = "Operational Error"
        if res:
           exc.key = res.key
           exc.result = res

        return exc

    def _invoke_common(self, fn, ctx, is_multi):
        err = fn(self._instance, ffi.NULL, *ctx.args())
        if err != C.LCB_SUCCESS:
            raise self._make_exc(err)

        self._cur.start(ctx)
        C.lcb_wait(self._instance)

        if self._cur.exc:
            self._cur.rethrow()

        return self._cur.mkret(is_multi)

    # Generate the 'set()' family of methods
    locals().update(gen_mutators())

    # Generate the simple getters
    locals().update(gen_simple())

    ### HTTP API ###
    def _http_complete_callback(self, htreq, instance, cookie, err, resp):
        res = HttpResult()
        cres = resp.v.v0

        res.htcode = cres.status
        res.rc = err
        priv = self._cur.res._priv

        # Get the headers?
        if priv['want_headers']:
            kvp = ffi.cast('char**', cres.headers)
            if kvp:
                curix = 0
                while kvp[curix] != ffi.NULL:
                    hdrname = ffi.string(kvp[curix])
                    hdrval = ffi.string(kvp[curix+1])
                    res.headers[hdrname] = hdrval
                    curix += 2

        fmt = priv['format']

        if cres.bytes:
            s_buf = ffi.buffer(cres.bytes, cres.nbytes)[:]
            try:
                res.http_data = self._tc.decode_value(s_buf, fmt)
            except:
                res.http_data = s_buf

        self._cur.add_single(res, '', self)


    def _http_request(self, type, method, path,
                      content_type="application/json",
                      post_data=None,
                      response_format=FMT_JSON,
                      quiet=False,
                      fetch_headers=False,
                      chunked=False,
                      rows_per_call=-1):


        if chunked:
            raise NotImplementedError("Streaming views not supported yet")

        self._cur.start(None)
        cmd = ffi.new('lcb_http_cmd_t*')

        s_path = ffi.new('char[]', path)
        s_content_type = ffi.new('char[]', content_type)
        s_body = None

        cmd.version = 0
        req = cmd.v.v0

        req.path = s_path
        req.npath = len(path)

        req.content_type = s_content_type

        if post_data:
            s_body = ffi.new('char[]', post_data)
            req.body = s_body
            req.nbody = len(post_data)

        else:
            req.body = ffi.NULL
            req.nbody = 0

        req.method = method
        req.chunked = 0

        self._cur.res._priv = {
            'format': response_format,
            'want_headers': fetch_headers
        }

        htreq_p = ffi.new('lcb_http_request_t*')
        err = C.lcb_make_http_request(self._instance,
                                      ffi.NULL, type, cmd, htreq_p)

        if err != C.LCB_SUCCESS:
            raise self._make_exc(err)

        C.lcb_wait(self._instance)
        res = self._cur.res.values()[0]

        if not quiet and not res.success:
            self._cur.rethrow()
            raise HTTPError.pyexc(res.http_data)

        return res

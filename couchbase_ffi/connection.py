from couchbase.transcoder import TranscoderPP
from couchbase.connection import Connection as _ExtConnection
from couchbase.user_constants import *
from couchbase.exceptions import (
    CouchbaseError,
    ValueFormatError,
    ArgumentError
)

from couchbase_ffi._cinit import get_handle, CALLBACK_DECLS
from couchbase_ffi.result import (MultiResult, OperationResult, ValueResult)
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
        ('touch', TouchCommandContext, C.lcb_touch)
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

    def add_single(self, pres, key, conn):
        pres.key = key
        try:
            self.res[key] = pres

        except TypeError as e:
            self.throw(ValueFormatError.pyexc("Unhashable key", obj=key))
            return

        if not pres.success:
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
                                   self._unlock_callback)
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

    @pycbc_cpy('stats')
    def stats(self, *args, **kwargs): pass

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

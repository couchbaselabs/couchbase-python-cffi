import sys
import warnings
from threading import Lock

from couchbase_ffi._cinit import get_handle
from couchbase_ffi.result import MultiResult, ObserveInfo, ValueResult
from couchbase_ffi.view import ViewResult
from couchbase_ffi.http import HttpRequest
from couchbase_ffi.iops import IOPSWrapper
from couchbase_ffi.lcbcntl import CNTL_VTYPE_MAP
from couchbase_ffi.bufmanager import BufManager
from couchbase_ffi._rtconfig import (
    PyCBC, pycbc_exc_enc, pycbc_exc_args, pycbc_exc_lcb)
from couchbase_ffi._strutil import from_cstring
import couchbase_ffi.executors as executors

from couchbase_ffi.constants import (
    FMT_JSON, PYCBC_CONN_F_CLOSED, PYCBC_CONN_F_WARNEXPLICIT,
    LOCKMODE_EXC, LOCKMODE_NONE)

ffi, C = get_handle()


CALLBACK_DECL = 'void(lcb_t,int,const lcb_RESPBASE*)'


def _make_transcoder():
    from couchbase.transcoder import TranscoderPP

    class _Transcoder(TranscoderPP):
        def _do_json_encode(self, value):
            return PyCBC.json_encode(value)

        def _do_json_decode(self, value):
            return PyCBC.json_decode(value)

        def _do_pickle_encode(self, value):
            return PyCBC.pickle_encode(value)

        def _do_pickle_decode(self, value):
            return PyCBC.pickle_decode(value)

    return _Transcoder()


def _gen_valmeth(name):
    def store_single(self, k, v, **kwargs):
        return self._execute_single_kv(name, k, v, **kwargs)
    def store_multi(self, kv, **kwargs):
        return self._execute_multi(name, kv, **kwargs)
    return store_single, store_multi


def _gen_keymeth(name):
    def do_single(self, k, **kwargs):
        return self._execute_single_k(name, k, **kwargs)
    def do_multi(self, kv, **kwargs):
        return self._execute_multi(name, kv, **kwargs)
    return do_single, do_multi


class Bucket(object):
    __slots__ = [
        # Private to cffi
        '_handles', '_lcbh', '_bound_cb', '_executors', '_iowrap',
        '__bucket', '_lock', '_lockmode', '_pipeline_queue',

        # Property holders
        '__default_format', '__quiet',

        # User-facing
        '__transcoder', 'data_passthrough',

        # Internal (used by couchbase and couchbase_ffi
        '_dur_persist_to', '_dur_replicate_to', '_dur_timeout', '_dur_testhook',
        '_privflags'
    ]

    @property
    def _tc(self):
        return self.__transcoder

    def __init__(self, connection_string=None, connstr=None,
                 username=None, password=None, quiet=False,
                 transcoder=None, default_format=FMT_JSON,
                 lockmode=LOCKMODE_EXC, unlock_gil=True,
                 _iops=None, _conntype=C.LCB_TYPE_BUCKET):

        crst = ffi.new('struct lcb_create_st*')
        bm = BufManager(ffi)

        if not connstr and not connection_string:
            raise pycbc_exc_args('Must have connection string')
        if connstr and connection_string:
            raise pycbc_exc_args(
                "Cannot specify both 'connstr' and 'connection_string'")
        if not connstr:
            connstr = connection_string

        crst.version = 3
        crst.v.v3.connstr = bm.new_cstr(connstr)
        crst.v.v3.passwd = bm.new_cstr(password)
        crst.v.v3.username = bm.new_cstr(username)
        crst.v.v3.type = _conntype

        if _iops:
            procs = _iops
            self._iowrap = IOPSWrapper(procs)
            crst.v.v3.io = self._iowrap.get_lcb_iops()
        else:
            crst.v.v3.io = ffi.NULL

        self._handles = set()

        lcb_pp = ffi.new('lcb_t*')
        rc = C.lcb_create(lcb_pp, crst)
        if rc != C.LCB_SUCCESS:
            raise pycbc_exc_lcb(rc)

        self._lcbh = lcb_pp[0]

        self._bound_cb = {
            'store': ffi.callback(CALLBACK_DECL, self._storage_callback),
            'get': ffi.callback(CALLBACK_DECL, self._get_callback),
            'remove': ffi.callback(CALLBACK_DECL, self._remove_callback),
            'counter': ffi.callback(CALLBACK_DECL, self._counter_callback),
            'observe': ffi.callback(CALLBACK_DECL, self._observe_callback),
            'stats': ffi.callback(CALLBACK_DECL, self._stats_callback),
            'http': ffi.callback(CALLBACK_DECL, self._http_callback),
            '_default': ffi.callback(CALLBACK_DECL, self._default_callback),
        }

        self._executors = {
            'upsert': executors.UpsertExecutor(self),
            'insert': executors.InsertExecutor(self),
            'replace': executors.ReplaceExecutor(self),
            'append': executors.AppendExecutor(self),
            'prepend': executors.PrependExecutor(self),
            'get': executors.GetExecutor(self),
            'lock': executors.LockExecutor(self),
            '_unlock': executors.UnlockExecutor(self),
            'touch': executors.TouchExecutor(self),
            'remove': executors.RemoveExecutor(self),
            'counter': executors.CounterExecutor(self),
            'endure': executors.DurabilityExecutor(self),
            '_chained_endure': executors.DurabilityChainExecutor(self),
            'observe': executors.ObserveExecutor(self),
            'stats': executors.StatsExecutor(self),
            '_rget': executors.GetReplicaExecutor(self)
        }

        self._install_cb(C.LCB_CALLBACK_DEFAULT, '_default')
        self._install_cb(C.LCB_CALLBACK_STORE, 'store')
        self._install_cb(C.LCB_CALLBACK_GET, 'get')
        self._install_cb(C.LCB_CALLBACK_GETREPLICA, 'get')
        self._install_cb(C.LCB_CALLBACK_REMOVE, 'remove')
        self._install_cb(C.LCB_CALLBACK_COUNTER, 'counter')
        self._install_cb(C.LCB_CALLBACK_OBSERVE, 'observe')
        self._install_cb(C.LCB_CALLBACK_STATS, 'stats')
        self._install_cb(C.LCB_CALLBACK_HTTP, 'http')

        # Set our properties
        self.data_passthrough = False
        self.__transcoder = transcoder or _make_transcoder()
        self.__default_format = FMT_JSON
        self.__quiet = False

        self.default_format = default_format
        self.quiet = quiet

        self._dur_persist_to = 0
        self._dur_replicate_to = 0
        self._dur_timeout = 0
        self._dur_testhook = None
        self._privflags = 0
        self.__bucket = self._cntl(C.LCB_CNTL_BUCKETNAME, value_type='string')

        if not unlock_gil:
            # We don't use this property, but tests depend on this
            lockmode = LOCKMODE_NONE
        self._lockmode = lockmode
        self._lock = Lock()
        self._pipeline_queue = None

    @property
    def default_format(self):
        return self.__default_format

    @default_format.setter
    def default_format(self, arg):
        if arg is PyCBC.fmt_auto:
            self.__default_format = arg
            return

        if isinstance(arg, bool):
            raise pycbc_exc_args('Must be a number', obj=arg)
        if not isinstance(arg, int):
            raise pycbc_exc_args('Must be a number', obj=arg)
        self.__default_format = arg

    @property
    def quiet(self):
        return self.__quiet
    @quiet.setter
    def quiet(self, arg):
        if isinstance(arg, bool):
            self.__quiet = arg
        else:
            raise pycbc_exc_args("'quiet' must be bool")

    @property
    def bucket(self):
        return self.__bucket

    @property
    def lockmode(self):
        return self._lockmode

    @property
    def transcoder(self):
        return self.__transcoder
    @transcoder.setter
    def transcoder(self, arg):
        if arg in (None, False):
            arg = _make_transcoder()
        self.__transcoder = arg

    def _install_cb(self, cbtype, name):
        C.lcb_install_callback3(self._lcbh, cbtype, self._bound_cb[name])

    def _connect(self):
        rc = C.lcb_connect(self._lcbh)
        if rc != C.LCB_SUCCESS:
            raise pycbc_exc_lcb(rc)

        C.lcb_wait(self._lcbh)
        rc = C.lcb_get_bootstrap_status(self._lcbh)
        if rc != C.LCB_SUCCESS:
            raise pycbc_exc_lcb(rc)

    def _make_mres(self):
        return MultiResult()

    def _do_lock(self):
        if self._lockmode == LOCKMODE_NONE:
            return
        elif self._lockmode == LOCKMODE_EXC:
            if not self._lock.acquire(False):
                raise PyCBC.exc_lock()
        else:
            self._lock.acquire(True)

    def _do_unlock(self):
        if self._lockmode != LOCKMODE_NONE:
            self._lock.release()

    def _thr_lockop(self, arg):
        # Used by tests
        if not self._lockmode:
            raise PyCBC.exc_lock()
        if not arg:
            self._lock.acquire(True)
        else:
            self._lock.release()

    def _chk_no_pipeline(self, msg='Pipeline active'):
        if self._pipeline_queue is not None:
            PyCBC.exc_pipeline(msg)

    def _pipeline_begin(self):
        self._chk_no_pipeline('Pipeline is already active')
        self._pipeline_queue = []

    def _pipeline_end(self):
        if self._pipeline_queue is None:
            PyCBC.exc_pipeline('No pipeline in progress!')

        C.lcb_wait(self._lcbh)
        results = self._pipeline_queue
        self._pipeline_queue = None
        rv = []

        for mres in results:
            mres._maybe_throw()
            if mres._is_single:
                rv.append(mres.unwrap_single())
            else:
                rv.append(mres)
        return rv

    def _run_sync(self, mres):
        self._handles.add(mres)
        if self._pipeline_queue is None:
            C.lcb_wait(self._lcbh)
            mres._maybe_throw()
        else:
            self._pipeline_queue.append(mres)
        return mres

    def _run_sync_single(self, mres):
        return self._run_sync(mres).unwrap_single()

    def _run_single(self, mres):
        return self._run_sync_single(mres)

    def _run_multi(self, mres):
        mres._is_single = False
        return self._run_sync(mres)

    def _execute_single_k(self, name, key, **kwargs):
        self._do_lock()
        try:
            proc = self._executors[name]
            mres = proc.execute((key,), **kwargs)
            return self._run_single(mres)
        finally:
            self._do_unlock()

    def _execute_single_kv(self, name, key, value, **kwargs):
        try:
            kv = {key: value}
        except TypeError:
            raise pycbc_exc_enc('Bad key-value', obj=(key,value))

        self._do_lock()
        try:
            proc = self._executors[name]
            mres = proc.execute(kv, **kwargs)
            return self._run_single(mres)
        finally:
            self._do_unlock()

    def _execute_multi(self, name, kv, **kwargs):
        self._do_lock()
        try:
            proc = self._executors[name]
            mres = proc.execute(kv, **kwargs)
            return self._run_multi(mres)
        finally:
            self._do_unlock()

    _VALUE_METHS = ['upsert', 'insert', 'replace', 'append', 'prepend']
    _KEY_METHS = ['get', 'lock', 'touch', 'remove', 'counter',
                  'observe', 'endure', '_rget', '_unlock']

    for name in _VALUE_METHS + _KEY_METHS:
        n_single = name
        n_multi = name + '_multi'
        if name in _VALUE_METHS:
            m_single, m_multi = _gen_valmeth(name)
        else:
            m_single, m_multi = _gen_keymeth(name)

        locals().update({n_single: m_single, n_multi: m_multi})

    def _stats(self, kv):
        return self._execute_multi('stats', kv)


    # Unlock is special:
    def unlock(self, key, cas, **kwargs):
        kwargs['cas'] = cas
        return self._unlock(key, **kwargs)

    unlock_multi = _unlock_multi
    _rgetix = _rget
    _rgetix_multi = _rget_multi

    def _view_request(self, design, view, options, include_docs):
        self._chk_no_pipeline('View requests not valid in pipeline mode')
        res = ViewResult(design, view, options, include_docs)
        mres = self._make_mres()
        mres[None] = res
        res._schedule(self, mres)
        return mres

    def _http_request(self, path, **kwargs):
        self._chk_no_pipeline('HTTP requests not valid in pipeline mode')
        htreq = HttpRequest(path, **kwargs)
        mres = self._make_mres()
        htreq._schedule(self, mres)
        self._handles.add(mres)
        return self._run_single(mres)

    def _cntlstr(self, cntl_key, cntl_value):
        rc = C.lcb_cntl_string(self._lcbh,
                               cntl_key.encode('utf-8'),
                               cntl_value.encode('utf-8'))
        if rc:
            raise pycbc_exc_lcb(rc)

    def _cntl(self, op, value_type=None, value=None):
        try:
            handler = CNTL_VTYPE_MAP[value_type]
        except KeyError:
            raise pycbc_exc_args('Invalid value type', obj=value_type)
        return handler.execute(self._lcbh, op, value)

    @property
    def _closed(self):
        return self._privflags & PYCBC_CONN_F_CLOSED

    def _close(self):
        if self._closed:
            return

        if self._lcbh:
            C.lcb_destroy(self._lcbh)
            lcb_pp = ffi.new('lcb_t*')
            C.lcb_create(lcb_pp, ffi.NULL)
            self._lcbh = lcb_pp[0]
            self._privflags |= PYCBC_CONN_F_CLOSED

    @property
    def server_nodes(self):
        nodelist = C.lcb_get_server_list(self._lcbh)
        s_list = []
        ix = 0

        while True:
            cur_str = nodelist[ix]
            if not cur_str:
                break
            s_list.append(from_cstring(cur_str))
            ix += 1

        return s_list

    def _chain_endure(self, optype, mres, result, dur):
        persist_to, replicate_to = dur
        proc = self._executors['_chained_endure']
        try:
            proc.execute(kv={result.key: result},
                         persist_to=persist_to, replicate_to=replicate_to,
                         check_removed=optype == C.LCB_CALLBACK_REMOVE,
                         _MRES=mres)
            return True

        except:
            mres._add_err(sys.exc_info())
            return False

    def _default_callback(self, *args):
        self._callback_common(*args)

    def _callback_common(self, instance, cbtype, resp, do_decr=True):
        mres = ffi.from_handle(resp.cookie)
        buf = bytes(ffi.buffer(resp.key, resp.nkey))
        try:
            key = self._tc.decode_key(buf)
            result = mres[key]
        except:
            raise pycbc_exc_enc(buf)

        result.rc = resp.rc
        if resp.rc:
            mres._add_bad_rc(resp.rc, result)
        else:
            result.cas = resp.cas

        if self._dur_testhook:
            self._dur_testhook(result)

        if cbtype != C.LCB_CALLBACK_ENDURE and mres._dur:
            if self._chain_endure(cbtype, mres, result, mres._dur):
                return None, None

        if do_decr and mres._decr_remaining():
            try:
                self._handles.remove(mres)
            except KeyError:
                # traceback.print_stack()
                raise

        return result, mres

    def _storage_callback(self, instance, cbtype, resp):
        self._callback_common(instance, cbtype, resp)

    def _get_callback(self, instance, cbtype, resp):
        result, mres = self._callback_common(instance, cbtype, resp)
        resp = ffi.cast('lcb_RESPGET*', resp)
        result.flags = resp.itmflags

        if not resp.rc:
            buf = bytes(ffi.buffer(resp.value, resp.nvalue))

            if not self.data_passthrough and not mres._no_format:
                try:
                    result.value = self._tc.decode_value(buf, resp.itmflags)
                except:
                    result.value = buf[::]
                    try:
                        raise pycbc_exc_enc(obj=buf)
                    except PyCBC.default_exception:
                        mres._add_err(sys.exc_info())
            else:
                result.value = buf[::]

    def _remove_callback(self, instance, cbtype, resp):
        self._callback_common(instance, cbtype, resp)

    def _counter_callback(self, instance, cbtype, resp):
        result, mres = self._callback_common(instance, cbtype, resp)
        if not resp.rc:
            resp = ffi.cast('lcb_RESPCOUNTER*', resp)
            result.value = resp.value

    def _observe_callback(self, instance, cbtype, resp):
        resp = ffi.cast('lcb_RESPOBSERVE*', resp)
        if resp.rflags & C.LCB_RESP_F_FINAL:
            mres = ffi.from_handle(resp.cookie)
            if mres._decr_remaining():
                self._handles.remove(mres)

            return

        rc = resp.rc
        result, mres = self._callback_common(
            instance, cbtype, resp, do_decr=False)

        if rc:
            if not result.rc:
                result.rc = rc
            return

        oi = ObserveInfo()
        oi.cas = resp.cas
        oi.flags = resp.status
        oi.from_master = resp.ismaster
        result.value.append(oi)

    def _stats_callback(self, instance, cbtype, resp):
        resp = ffi.cast('lcb_RESPSTATS*', resp)
        mres = ffi.from_handle(resp.cookie)

        if resp.rc:
            r = ValueResult()
            r.key = '__dummy__'
            mres._add_bad_rc(resp.rc, r)

        if resp.key == ffi.NULL and resp.server == ffi.NULL:
            if mres._decr_remaining():
                self._handles.remove(mres)
            return

        if resp.rc:
            return

        kbuf = bytes(ffi.buffer(resp.key, resp.nkey))
        key = self._tc.decode_key(kbuf)
        if resp.nvalue:
            value = from_cstring(resp.value, resp.nvalue)
            try:
                value = int(value)
            except ValueError:
                pass
        else:
            value = None

        server = from_cstring(resp.server)
        mres.setdefault(key, {})[server] = value

    def _http_callback(self, instance, cbtype, resp):
        mres = ffi.from_handle(resp.cookie)
        resp = ffi.cast('lcb_RESPHTTP*', resp)
        htres = mres[None]
        self._handles.remove(mres)
        htres._handle_response(mres, resp)

    def __del__(self):
        if hasattr(self, '_lcbh') and self._lcbh:
            C.lcb_destroy(self._lcbh)
            self._lcbh = None

    def _warn_dupkey(self, k):
        """
        Really odd function - used to help ensure we actually warn for duplicate
        keys.
        """
        if self._privflags & PYCBC_CONN_F_WARNEXPLICIT:
            warnings.warn_explicit(
                'Found duplicate keys! {0}'.format(k), RuntimeWarning,
                __file__, -1, module='couchbase_ffi.bucket', registry={})
        else:
            warnings.warn('Found duplicate keys!', RuntimeWarning)
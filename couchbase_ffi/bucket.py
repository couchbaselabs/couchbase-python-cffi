import sys
import warnings
import weakref
from threading import Lock

from couchbase._pyport import xrange

from couchbase_ffi._cinit import get_handle
from couchbase_ffi.result import (
    MultiResult, ObserveInfo, ValueResult, AsyncResult, _SDResult
)
from couchbase_ffi.view import ViewResult
from couchbase_ffi.n1ql import N1qlResult
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
    LOCKMODE_EXC, LOCKMODE_NONE, PYCBC_CONN_F_ASYNC)

ffi, C = get_handle()


CALLBACK_DECL = 'void(lcb_t,int,lcb_RESPBASE*)'


def _make_transcoder():
    # noinspection PyUnresolvedReferences
    from couchbase_ffi._libcouchbase import Transcoder
    return Transcoder()


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


class InstanceReference(weakref.ref):
    """
    This magical class exists because we can't really have a __del__ method
    without actually leaking all over the place. This allows us to cooperate
    with python's cyclic GC, while ensuring that the underlying C handle gets
    freed when the object is no longer in scope.

    Note that while we could use FFI's 'gc' functionality, this wouldn't help
    us with all the custom dtor hooks and such (which are embedded into the
    tests).

    Use the `dtorhook` property to register your own callback. The callback
    will be invoked after the underlying C handle is destroyed.
    """
    INSTANCES = {}

    def __new__(cls, bucket):
        instance = bucket._lcbh
        ret = weakref.ref.__new__(cls, bucket, lambda x: x._dtor())
        cls.INSTANCES[instance] = ret
        return ret

    def _invoke_hooks(self):
        if self.dtorhook:
            self.dtorhook()

    def _async_dtor_cb(self, *_):
        self._invoke_hooks()
        del self.INSTANCES[self.instance]

    def _dtor(self):
        if self.instance not in self.INSTANCES:
            self._invoke_hooks()
            return

        if not self._is_async:
            C.lcb_destroy(self.instance)
            if self.dtorhook:
                self.dtorhook()
                del self.INSTANCES[self.instance]
        else:
            C.lcb_set_destroy_callback(self.instance, self._boundcb)
            C.lcb_destroy_async(self.instance, ffi.NULL)

    def __init__(self, bucket):
        self.dtorhook = None
        self._is_async = bucket._is_async
        self._boundcb = ffi.callback('void(void*)', self._async_dtor_cb)
        self.instance = bucket._lcbh

    @classmethod
    def delref(cls, bucket):
        """
        Clears the instance reference for a given bucket.

        This should be called if destroying the `lcb_t` handle manually.
        :param bucket: The bucket
        """
        del cls.INSTANCES[bucket._lcbh]

    @classmethod
    def getref(cls, bucket):
        """
        Retrieves the :class:`InstanceReference` object associated with
        the provided `bucket`. The bucket must have previously registered
        itself via :meth:`addref`
        :param bucket: The bucket
        :return: The InstanceReference object
        """
        return cls.INSTANCES[bucket._lcbh]

    @classmethod
    def addref(cls, bucket):
        """
        Adds the bucket's lcb_t to be destroyed when the bucket is
        destroyed. To add special hooks, simply call the :meth:getref()
        """
        return cls(bucket)


class Bucket(object):
    # I'm using slots here because i have a LOT of attributes and I want to
    # make sure i'm not assigning to anything silly:

    __slots__ = [
        # Private to cffi
        '_handles', '_lcbh', '_bound_cb', '_executors', '_iowrap',
        '__bucket', '_lock', '_lockmode', '_pipeline_queue',
        '_embedref', '_waiting',

        # Property holders
        '__default_format', '__quiet', '__connected', '__dtor_handle',

        # User-facing
        '__transcoder', '__is_default_tc', 'data_passthrough', 'unlock_gil',

        # Internal (used by couchbase and couchbase_ffi
        '_dur_persist_to', '_dur_replicate_to', '_dur_timeout', '_dur_testhook',
        '_privflags', '_conncb', '_sd_entry', '_sd_iterpos'
    ]

    @property
    def _tc(self):
        return self.__transcoder

    def __init__(self, connection_string=None, connstr=None,
                 username=None, password=None, quiet=False,
                 transcoder=None, default_format=FMT_JSON,
                 lockmode=LOCKMODE_EXC, unlock_gil=True,
                 _iops=None, _conntype=C.LCB_TYPE_BUCKET,
                 _flags=0):

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
            'subdoc': ffi.callback(CALLBACK_DECL, self._subdoc_callback),
            'remove': ffi.callback(CALLBACK_DECL, self._remove_callback),
            'counter': ffi.callback(CALLBACK_DECL, self._counter_callback),
            'observe': ffi.callback(CALLBACK_DECL, self._observe_callback),
            'stats': ffi.callback(CALLBACK_DECL, self._stats_callback),
            'http': ffi.callback(CALLBACK_DECL, self._http_callback),
            '_default': ffi.callback(CALLBACK_DECL, self._default_callback),
            '_bootstrap': ffi.callback('void(lcb_t,lcb_error_t)',
                                       self._bootstrap_callback),
            '_dtor': ffi.callback('void(void*)',
                                  self._instance_destroyed)
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
            '_rget': executors.GetReplicaExecutor(self),
            'lookup_in': executors.SubdocLookupExecutor(self),
            'mutate_in': executors.SubdocMutationExecutor(self)
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
        self._install_cb(C.LCB_CALLBACK_SDLOOKUP, 'subdoc')
        self._install_cb(C.LCB_CALLBACK_SDMUTATE, 'subdoc')
        C.lcb_set_bootstrap_callback(self._lcbh, self._bound_cb['_bootstrap'])

        # Set our properties
        self.data_passthrough = False
        self.transcoder = transcoder
        self.default_format = default_format
        self.quiet = quiet
        self.unlock_gil = unlock_gil

        self._dur_persist_to = 0
        self._dur_replicate_to = 0
        self._dur_timeout = 0
        self._dur_testhook = None
        self._privflags = _flags
        self._conncb = None
        self.__bucket = self._cntl(C.LCB_CNTL_BUCKETNAME, value_type='string')
        self.__connected = False
        self._lockmode = lockmode if unlock_gil else LOCKMODE_NONE
        self._lock = Lock()
        self._pipeline_queue = None
        self._waiting = False

        self._embedref = None
        InstanceReference.addref(self)

        self._sd_entry = ffi.new('lcb_SDENTRY*')
        self._sd_iterpos = ffi.new('size_t*')

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
        return None if self.__is_default_tc else self.__transcoder

    @transcoder.setter
    def transcoder(self, arg):
        if arg in (None, False):
            self.__transcoder = _make_transcoder()
            self.__is_default_tc = True
        else:
            self.__transcoder = arg
            self.__is_default_tc = True

    @property
    def _is_async(self):
        return self._privflags & PYCBC_CONN_F_ASYNC

    @property
    def connected(self):
        return self.__connected

    @property
    def _wref(self):
        return self._embedref if self._embedref \
            else InstanceReference.getref(self)

    @property
    def _dtorcb(self):
        return self._wref.dtorhook

    @_dtorcb.setter
    def _dtorcb(self, newval):
        self._wref.dtorhook = newval

    def _make_mres(self):
        if self._is_async:
            return AsyncResult()
        else:
            return MultiResult()

    def _install_cb(self, cbtype, name):
        C.lcb_install_callback3(self._lcbh, cbtype, self._bound_cb[name])

    def _connect(self):
        rc = C.lcb_connect(self._lcbh)
        if rc != C.LCB_SUCCESS:
            raise pycbc_exc_lcb(rc)

        if self._is_async:
            return

        C.lcb_wait(self._lcbh)
        rc = C.lcb_get_bootstrap_status(self._lcbh)
        if rc != C.LCB_SUCCESS:
            raise pycbc_exc_lcb(rc)
        self.__connected = True

    def _bootstrap_callback(self, _, status):
        arg = None
        self.__connected = True
        if status != C.LCB_SUCCESS:
            try:
                raise pycbc_exc_lcb(status)
            except Exception as e:
                # Note _libcouchbase.so does this as well!
                arg = e

        if self._conncb:
            cb = self._conncb
            self._conncb = None
            cb(arg)

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
            self._waiting = True
            try:
                C.lcb_wait(self._lcbh)
            finally:
                self._waiting = False
            mres._maybe_throw()
        else:
            self._pipeline_queue.append(mres)
        return mres

    def _run_async(self, mres):
        self._handles.add(mres)
        return mres

    def _run_sync_single(self, mres):
        return self._run_sync(mres).unwrap_single()

    def _run_single(self, mres):
        if not self._is_async:
            return self._run_sync_single(mres)
        else:
            return self._run_async(mres)

    def _run_multi(self, mres):
        mres._is_single = False
        if not self._is_async:
            return self._run_sync(mres)
        else:
            return self._run_async(mres)

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

    _VALUE_METHS = ['upsert', 'insert', 'replace', 'append', 'prepend',
                    'mutate_in']
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

    # This name is used by couchbase.bucket.Bucket
    def _stats(self, kv, keystats=False):
        return self._execute_multi('stats', kv, keystats=keystats)

    # Unlock is special since we document the bare second arg as meaning
    # the CAS
    def unlock(self, key, cas, **kwargs):
        kwargs['cas'] = cas
        return self._unlock(key, **kwargs)

    # noinspection PyUnresolvedReferences
    unlock_multi = _unlock_multi
    # noinspection PyUnresolvedReferences
    _rgetix = _rget
    # noinspection PyUnresolvedReferences
    _rgetix_multi = _rget_multi

    def lookup_in_multi(self, kv, **kw):
        return self._execute_multi('lookup_in', kv, **kw)

    def lookup_in(self, keyspec, **kwargs):
        # Extract the key from the specs
        from couchbase._pyport import single_dict_key
        k = single_dict_key(keyspec)
        specs = keyspec[k]
        return self._execute_single_kv('lookup_in', k, specs, **kwargs)

    def _view_request(self, design, view, options, _flags=0):
        self._chk_no_pipeline('View requests not valid in pipeline mode')
        return ViewResult.init_with_mres(
            self._make_mres(), self,
            design, view, options, _flags=_flags)

    def _n1ql_query(self, body, adhoc):
        self._chk_no_pipeline('N1ql queries not valid in pipeline mode')
        return N1qlResult.init_with_mres(
            self._make_mres(), self, body, adhoc)

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

    OLD_CNTL_MAP = {
        0x00: 'uint32_t',
        0x01: 'uint32_t'
    }

    def _cntl(self, op, value=None, value_type=None):
        if value_type is None and op in self.OLD_CNTL_MAP:
            value_type = self.OLD_CNTL_MAP[op]
        try:
            handler = CNTL_VTYPE_MAP[value_type]
        except KeyError:
            raise pycbc_exc_args('Invalid value type', obj=value_type)
        return handler.execute(self._lcbh, op, value)

    def _vbmap(self, key):
        bm = BufManager(ffi)
        info_obj = ffi.new('lcb_cntl_vbinfo_t*')
        info_obj.v.v0.key, info_obj.v.v0.nkey = bm.new_cbuf(key)
        rc = C.lcb_cntl(self._lcbh, C.LCB_CNTL_GET, C.LCB_CNTL_VBMAP, info_obj)
        if rc:
            raise pycbc_exc_lcb(rc)
        return info_obj.v.v0.vbucket, info_obj.v.v0.server_index

    @property
    def _closed(self):
        return self._privflags & PYCBC_CONN_F_CLOSED

    @property
    def waiting(self):
        return self._waiting

    def _close(self, is_async=False):
        if self._closed or not self._lcbh:
            return

        # Delete the reference to ourselves
        wref = InstanceReference.getref(self)
        InstanceReference.delref(self)
        self._embedref = wref

        if not is_async:
            C.lcb_destroy(self._lcbh)
        else:
            C.lcb_set_destroy_callback(self._lcbh, self._bound_cb['_dtor'])
            C.lcb_destroy_async(self._lcbh, ffi.NULL)

        lcb_pp = ffi.new('lcb_t*')
        C.lcb_create(lcb_pp, ffi.NULL)
        self._lcbh = lcb_pp[0]
        self._privflags |= PYCBC_CONN_F_CLOSED

    def _instance_destroyed(self, _):
        if self._dtorcb:
            self._dtorcb()
            self._dtorcb = None

    def _async_shutdown(self):
        self._close(is_async=True)

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

    def _chk_op_done(self, mres):
        if not mres:
            return
        if not mres._decr_remaining():
            return
        # So the result is complete
        self._handles.remove(mres)
        if self._is_async:
            mres.invoke()

    def _set_mutinfo(self, result, optype, rb):
        if not result.success:
            return
        mt = C.lcb_resp_get_mutation_token(optype, rb)
        if mt != ffi.NULL:
            mt = (C._Cb_mt_vb(mt), C._Cb_mt_uuid(mt), C._Cb_mt_seq(mt),
                  self.__bucket)
            result._mutinfo = mt

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
        _, mres = self._callback_common(*args)
        self._chk_op_done(mres)

    def _callback_common(self, _, cbtype, resp, is_mutator=False):
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
            if is_mutator:
                self._set_mutinfo(result, cbtype,
                                  ffi.cast('lcb_RESPBASE*', resp))

        if self._dur_testhook:
            self._dur_testhook(result)

        if cbtype != C.LCB_CALLBACK_ENDURE and mres._dur:
            if self._chain_endure(cbtype, mres, result, mres._dur):
                return None, None

        return result, mres

    def _storage_callback(self, instance, cbtype, resp):
        _, mres = self._callback_common(instance, cbtype, resp, is_mutator=True)
        self._chk_op_done(mres)

    def _subdoc_callback(self, instance, cbtype, rb):
        resp = ffi.cast('lcb_RESPSUBDOC*', rb)
        mres = ffi.from_handle(resp.cookie)
        buf = bytes(ffi.buffer(resp.key, resp.nkey))
        try:
            key = self._tc.decode_key(buf)
            result = mres[key]  # type: _SDResult
        except:
            raise pycbc_exc_enc(buf)

        result.rc = resp.rc
        if resp.rc not in (C.LCB_SUCCESS, C.LCB_SUBDOC_MULTI_FAILURE):
            mres._add_bad_rc(resp.rc, result)
            self._chk_op_done(mres)
            return
        else:
            result.cas = resp.cas

        # naming conventions as in the Couchbase C extension
        cur = self._sd_entry
        vii = self._sd_iterpos
        vii[0] = 0  # Reset iterator
        oix = 0

        is_mutate = cbtype == C.LCB_CALLBACK_SDMUTATE
        while C.lcb_sdresult_next(resp, cur, vii) != 0:
            if is_mutate:
                cur_index = cur.index
            else:
                cur_index = oix
                oix += 1
            if cur.status == 0 and cur.nvalue:
                buf = bytes(ffi.buffer(cur.value, cur.nvalue))
                try:
                    value = self._tc.decode_value(buf, FMT_JSON)
                except:
                    raise pycbc_exc_enc(obj=buf)
            else:
                value = None

            cur_tuple = (cur.status, value)
            if cur.status:
                if is_mutate or cur.status != C.LCB_SUBDOC_PATH_ENOENT:
                    spec = result._specs[cur_index]
                    try:
                        raise pycbc_exc_lcb(cur.status, 'Subcommand failure', obj=spec)
                    except PyCBC.default_exception:
                        mres._add_err(sys.exc_info())

            result._add_result(cur_index, cur_tuple)

        if is_mutate and result.success:
            self._set_mutinfo(result, cbtype, rb)
            if mres._dur and self._chain_endure(cbtype, mres, result, mres._dur):
                return

        self._chk_op_done(mres)

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

        self._chk_op_done(mres)

    def _remove_callback(self, instance, cbtype, resp):
        _, mres = self._callback_common(instance, cbtype, resp, is_mutator=True)
        self._chk_op_done(mres)

    def _counter_callback(self, instance, cbtype, resp):
        result, mres = self._callback_common(
            instance, cbtype, resp, is_mutator=True)
        if not resp.rc:
            resp = ffi.cast('lcb_RESPCOUNTER*', resp)
            result.value = resp.value
        self._chk_op_done(mres)

    def _observe_callback(self, instance, cbtype, resp):
        resp = ffi.cast('lcb_RESPOBSERVE*', resp)
        if resp.rflags & C.LCB_RESP_F_FINAL:
            mres = ffi.from_handle(resp.cookie)
            self._chk_op_done(mres)
            return

        rc = resp.rc
        result, mres = self._callback_common(instance, cbtype, resp)

        if rc:
            if not result.rc:
                result.rc = rc
            return

        oi = ObserveInfo()
        oi.cas = resp.cas
        oi.flags = resp.status
        oi.from_master = resp.ismaster
        result.value.append(oi)

    # noinspection PyUnusedLocal
    def _stats_callback(self, instance, cbtype, resp):
        resp = ffi.cast('lcb_RESPSTATS*', resp)
        mres = ffi.from_handle(resp.cookie)

        if resp.rc:
            r = ValueResult()
            r.key = '__dummy__'
            mres._add_bad_rc(resp.rc, r)

        if resp.key == ffi.NULL and resp.server == ffi.NULL:
            self._chk_op_done(mres)
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

    def _mutinfo(self):
        pp = ffi.new('void**')
        kb = ffi.new('lcb_KEYBUF*')

        rc = C.lcb_cntl(self._lcbh, C.LCB_CNTL_GET, C.LCB_CNTL_VBCONFIG, pp)
        if rc:
            pycbc_exc_lcb(rc, "Couldn't get vBucket config")
        nvb = C.vbucket_config_get_num_vbuckets(pp[0])
        ll = []
        kb.type = C.LCB_KV_VBID

        for vbid in xrange(nvb):
            kb.contig.nbytes = vbid
            mt = C.lcb_get_mutation_token(self._lcbh, kb, ffi.NULL)
            if not mt:
                continue
            ll.append((C._Cb_mt_vb(mt), C._Cb_mt_uuid(mt), C._Cb_mt_seq(mt)))

        return ll

    def _add_creds(self, user, password):
        bm = BufManager(ffi)
        c_user = bm.new_cstr(user)
        c_pass = bm.new_cstr(password)
        pp = ffi.new('char*[2]', (c_user, c_pass))
        rc = C.lcb_cntl(self._lcbh, C.LCB_CNTL_SET, C.LCB_CNTL_BUCKET_CRED, pp)
        if rc:
            pycbc_exc_lcb(rc)
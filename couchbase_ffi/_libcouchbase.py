from __future__ import print_function
from couchbase_ffi._rtconfig import PyCBC
from couchbase_ffi.c import get_handle
from couchbase_ffi._strutil import from_cstring
import couchbase_ffi.constants as constants

# noinspection PyUnresolvedReferences
from couchbase_ffi.iops import Event, IOEvent, TimerEvent


ffi, C = get_handle()

_IMPL_INCLUDE_DOCS = True


def lcb_version():
    num_p = ffi.new('unsigned*')
    str_p = C.lcb_get_version(num_p)
    return from_cstring(str_p), num_p[0]


def _modify_helpers(**kw):
    ret = {}
    for k, v in kw.items():
        ret[k] = PyCBC.get(k)
        PyCBC.configure(k, v)

    # print("Modification requested!")
    return ret


def _init_helpers(**kv):
    # import traceback
    # traceback.print_stack()
    # print("Bootstrap invoked!")
    _modify_helpers(**kv)
    # One special item still needs importing
    import couchbase
    couchbase.FMT_AUTO = kv['fmt_auto']
    constants.FMT_AUTO = kv['fmt_auto']


def _get_helper(k):
    return PyCBC.get(k)


def _strerror(rc):
    return from_cstring(C.lcb_strerror(ffi.NULL, rc))


def _get_errtype(rc):
    return C.lcb_get_errtype(rc)


# noinspection PyUnresolvedReferences
def _stage2_bootstrap():
    """
    This is the second bootstrap stage. It should be called
    _immediately_ after importing this module the first time. The
    reason behind this process is to allow this module to be inserted
    as a replacement for 'couchbase._libcouchbase' while not loading
    dependencies which depend on that name. The stage2 loads these
    dependencies which ultimately depend on ourselves :)
    """
    from couchbase_ffi.result import (
        Item,
        Result,
        ObserveInfo,
        MultiResult,
        ValueResult,
        OperationResult,
        HttpResult,
        AsyncResult,
        _SDResult
    )

    globals().update(locals())
    from couchbase_ffi.bucket import Bucket
    globals()['Bucket'] = Bucket

    from couchbase import _bootstrap
    globals()['Transcoder'] = None
    import couchbase.transcoder

    class _Transcoder(couchbase.transcoder.TranscoderPP):
        def _do_json_encode(self, value):
            return PyCBC.json_encode(value)

        def _do_json_decode(self, value):
            return PyCBC.json_decode(value)

        def _do_pickle_encode(self, value):
            return PyCBC.pickle_encode(value)

        def _do_pickle_decode(self, value):
            return PyCBC.pickle_decode(value)

    globals()['Transcoder'] = _Transcoder
    couchbase.transcoder.Transcoder = _Transcoder


pycbc_log_handler = None


@ffi.def_extern()
def _Cb_log_handlerPy(objid, subsys, severity, srcfile, srcline, msg):
    if not pycbc_log_handler:
        return
    pycbc_log_handler({
        'message': msg,
        'id': objid,
        'level': severity,
        'c_src': (srcfile, srcline),
        'subsys': subsys
    })


def lcb_logging(*args):
    global pycbc_log_handler
    if args:
        pycbc_log_handler, = args
    return pycbc_log_handler


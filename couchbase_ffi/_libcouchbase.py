from __future__ import print_function
from couchbase_ffi._rtconfig import PyCBC
from couchbase_ffi._cinit import get_handle
from couchbase_ffi._strutil import from_cstring
import couchbase_ffi.constants as constants

# noinspection PyUnresolvedReferences
from couchbase_ffi.iops import Event, IOEvent, TimerEvent


ffi, C = get_handle()

_IMPL_INCLUDE_DOCS=True


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


def _stage2_bootstrap():
    """
    This is the second bootstrap stage. It should be called
    _immediately_ after importing this module the first time. The
    reason behind this process is to allow this module to be inserted
    as a replacement for 'couchbase._libcouchbase' while not loading
    dependencies which depend on that name. The stage2 loads these
    dependencies which ultimately depend on ourselves :)
    """
    # noinspection PyUnresolvedReferences
    from couchbase_ffi.result import (
        Item,
        Result,
        ObserveInfo,
        MultiResult,
        ValueResult,
        OperationResult,
        HttpResult,
        AsyncResult
    )

    globals().update(locals())
    from couchbase_ffi.bucket import Bucket
    globals()['Bucket'] = Bucket
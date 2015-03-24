from couchbase_ffi._cinit import get_handle
from couchbase_ffi._rtconfig import pycbc_exc_lcb
from couchbase_ffi.bufmanager import BufManager

ffi, C = get_handle()

class _N1QLParams(object):
    def __init__(self):
        self._lp = ffi.gc(C.lcb_n1p_new(), C.lcb_n1p_free)

    def setquery(self, query=None, type=C.LCB_N1P_QUERY_STATEMENT):
        bm = BufManager(ffi)
        query = bm.new_cbuf(query)
        rc = C.lcb_n1p_setquery(self._lp, bm.new_cstr(query), len(query), type)
        if rc:
            raise pycbc_exc_lcb(rc)

    def setoption(self, option, value):
        bm = BufManager(ffi)
        option = bm.new_cbuf(option)
        value = bm.new_cbuf(value)
        rc = C.lcb_n1p_setopt(self._lp, option, len(option), value, len(value))
        if rc:
            raise pycbc_exc_lcb(rc)

    def set_namedarg(self, arg, value):
        bm = BufManager(ffi)
        arg = bm.new_cbuf(arg)
        value = bm.new_cbuf(value)
        rc = C.lcb_n1p_namedparam(self._lp, arg, len(arg), value, len(value))
        if rc:
            raise pycbc_exc_lcb(rc)

    def add_posarg(self, arg):
        bm = BufManager(ffi)
        arg = bm.new_cbuf(arg)
        rc = C.lcb_n1p_posparam(self._lp, arg, len(arg))
        if rc:
            raise pycbc_exc_lcb(rc)

    def clear(self):
        C.lcb_n1p_reset(self._lp)
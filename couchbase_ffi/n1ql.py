import sys

from couchbase_ffi.c import get_handle
from couchbase_ffi._rtconfig import pycbc_exc_lcb, PyCBC
from couchbase_ffi.bufmanager import BufManager
from couchbase_ffi.rowapi import RowResult

ffi, C = get_handle()


class N1qlResult(RowResult):
    def __init__(self, parent, params, prepare, mres=None):
        super(N1qlResult, self).__init__(parent)
        self._bound_cb = ffi.callback(
            'void(lcb_t,int,lcb_RESPN1QL*)', self._on_single_row)
        bm = BufManager(ffi)

        cmd = ffi.new('lcb_CMDN1QL*')
        cmd.query, cmd.nquery = bm.new_cbuf(params)
        cmd.callback = self._bound_cb
        if prepare:
            cmd.cmdflags |= C.LCB_CMDN1QL_F_PREPCACHE
        rc = C.lcb_n1ql_query(parent._lcbh, mres._cdata, cmd)
        if rc:
            raise pycbc_exc_lcb(rc)

    def _on_single_row(self, instance, cbtype, resp):
        mres = ffi.from_handle(resp.cookie)
        if resp.rflags & C.LCB_RESP_F_FINAL:
            if resp.nrow:
                self.value = bytes(ffi.buffer(resp.row, resp.nrow))
            self._step(mres, True)
            self._done(mres, resp.rc,
                       resp.htresp.htstatus if resp.htresp else 0)
        else:
            # Simply parse the row
            try:
                row = PyCBC.json_decode(bytes(ffi.buffer(resp.row, resp.nrow)))
                self.rows.append(row)
            except:
                mres._add_err(sys.exc_info())

        self._step(mres, False)

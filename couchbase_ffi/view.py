import sys

from couchbase_ffi._cinit import get_handle
from couchbase_ffi.result import ValueResult
from couchbase_ffi._rtconfig import pycbc_exc_lcb, PyCBC
from couchbase_ffi.bufmanager import BufManager
from couchbase_ffi._strutil import from_cstring
from couchbase_ffi.rowapi import RowResult

ffi, C = get_handle()

ROWCB_DECL = 'void(lcb_t,int,const lcb_RESPVIEWQUERY*)'


def mres2vres(mres):
    return mres[None]


def buf2str(v, n):
    return from_cstring(ffi.cast('const char*', v), n)


class ViewResult(RowResult):
    def __init__(self, parent, ddoc, view, options, _flags=0, mres=None):
        super(ViewResult, self).__init__(parent)
        self._ddoc = ddoc
        self._view = view
        self._bound_cb = ffi.callback(ROWCB_DECL, self._on_single_row)

        bm = BufManager(ffi)
        urlopts = ffi.NULL
        pypost = None
        cmd = ffi.new('lcb_CMDVIEWQUERY*')

        if options:
            in_uri, in_post = options._long_query_encoded
            # Note, encoded means URI/JSON encoded; not charset
            urlopts = bm.new_cstr(in_uri)
            if in_post and in_post != '{}':
                pypost = in_post

        C.lcb_view_query_initcmd(
            cmd, bm.new_cstr(self._ddoc), bm.new_cstr(self._view),
            urlopts, self._bound_cb)

        if pypost:
            cmd.postdata, cmd.npostdata = bm.new_cbuf(pypost)

        cmd.cmdflags |= _flags

        rc = C.lcb_view_query(self._instance, mres._cdata, cmd)
        if rc:
            raise pycbc_exc_lcb(rc)

    @property
    def key(self):
        return 'VIEW[{0}/{1}]'.format(self._ddoc, self._view)

    def _on_single_row(self, instance, cbtype, resp):
        mres = ffi.from_handle(resp.cookie)
        if resp.rflags & C.LCB_RESP_F_FINAL:
            if resp.nvalue:
                self.value = bytes(ffi.buffer(resp.value, resp.nvalue))
            self._step(mres, True)
            self._done(mres, resp.rc,
                       resp.htresp.htstatus if resp.htresp else 0)
            return

        # Actually parse the row here!
        row = {}
        if resp.nkey:
            row['key'] = PyCBC.json_decode(buf2str(resp.key, resp.nkey))
        if resp.nvalue:
            row['value'] = PyCBC.json_decode(buf2str(resp.value, resp.nvalue))
        if resp.docid:
            # Document ID is always a simple string, so no need to decode
            row['id'] = buf2str(resp.docid, resp.ndocid)

        if resp.docresp:
            py_doc = ValueResult()
            l_doc = resp.docresp
            row['__DOCRESULT__'] = py_doc
            py_doc.key = row['id']
            py_doc.flags = l_doc.itmflags
            py_doc.cas = l_doc.cas
            py_doc.rc = l_doc.rc
            if not resp.docresp.rc:
                buf = bytes(ffi.buffer(l_doc.value, l_doc.nvalue))
                try:
                    tc = self._parent._tc
                    py_doc.value = tc.decode_value(buf, py_doc.flags)
                except:
                    py_doc.value = buf[::]

        # So now that we have a row..
        self.rows.append(row)
        self._step(mres, False)
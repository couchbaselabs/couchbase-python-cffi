import sys

from couchbase_ffi._cinit import get_handle
from couchbase_ffi.result import ValueResult, Result
from couchbase_ffi._rtconfig import pycbc_exc_lcb, PyCBC
from couchbase_ffi.bufmanager import BufManager
from couchbase_ffi._strutil import from_cstring

ffi, C = get_handle()

ROWCB_DECL = 'void(lcb_t,int,const lcb_RESPVIEWQUERY*)'


def mres2vres(mres):
    return mres[None]


def buf2str(v, n):
    return from_cstring(ffi.cast('const char*', v), n)


class ViewResult(Result):
    def __init__(self, ddoc, view, options, include_docs=False):
        self._c_command = ffi.new('lcb_CMDVIEWQUERY*')
        self._c_handle = ffi.new('lcb_VIEWHANDLE*')
        self._ddoc = ddoc
        self._view = view
        self._options = options
        self._include_docs = include_docs
        self._parent = None
        self._rows = []
        self._rows_per_call = 0
        self._bound_cb = ffi.callback(ROWCB_DECL, self._on_single_row)
        self.done = False
        self.value = None
        self.http_status = 0

    @property
    def key(self):
        return 'VIEW[{0}/{1}]'.format(self._ddoc, self._view)

    def _schedule(self, parent, mres):
        bm = BufManager(ffi)
        urlopts = ffi.NULL
        pypost = None
        cmd = self._c_command

        if self._options:
            in_uri, in_post = self._options._long_query_encoded
            # Note, encoded means URI/JSON encoded; not charset
            urlopts = bm.new_cstr(in_uri)
            if in_post and in_post != '{}':
                pypost = in_post

        C.lcb_view_query_initcmd(
            cmd, bm.new_cstr(self._ddoc), bm.new_cstr(self._view),
            urlopts, self._bound_cb)

        if pypost:
            cmd.postdata, cmd.npostdata = bm.new_cbuf(pypost)

        if self._include_docs:
            cmd.cmdflags |= C.LCB_CMDVIEWQUERY_F_INCLUDE_DOCS

        self._c_command.handle = self._c_handle

        self._parent = parent
        rc = C.lcb_view_query(parent._lcbh, mres._cdata, self._c_command)
        if rc:
            raise pycbc_exc_lcb(rc)

    def _handle_done(self, resp, mres):
        self.done = True
        self._c_handle = None
        if resp.rc:
            if resp.rc == C.LCB_HTTP_ERROR:
                try:
                    raise PyCBC.exc_http(self.value)
                except:
                    mres._add_err(sys.exc_info())
            else:
                mres._add_bad_rc(resp.rc, self)

        if resp.nvalue:
            self.value = buf2str(resp.value, resp.nvalue)
            try:
                self.value = PyCBC.json_decode(self.value)
            except:
                pass

        if resp.htresp:
            if not self.value and resp.htresp.nbody:
                self.value = buf2str(resp.htresp.body, resp.htresp.nbody)
            self.http_status = resp.htresp.htstatus

    def _on_single_row(self, instance, cbtype, resp):
        mres = ffi.from_handle(resp.cookie)
        if resp.rflags & C.LCB_RESP_F_FINAL:
            self._handle_done(resp, mres)
            return

        if resp.rc != C.LCB_SUCCESS:
            mres._add_bad_rc(resp.rc, self)
            return

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
        self._rows.append(row)

    def fetch(self, mres):
        C.lcb_wait(self._parent._lcbh)
        ret = self._rows
        self._rows = []
        mres._maybe_throw()
        return ret


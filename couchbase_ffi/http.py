import sys

from couchbase_ffi.c import get_handle
from couchbase_ffi._rtconfig import PyCBC
from couchbase_ffi.constants import FMT_JSON
from couchbase_ffi.result import HttpResult
from couchbase_ffi.bufmanager import BufManager
from couchbase_ffi._strutil import from_cstring

ffi, C = get_handle()
METHOD_MAP = {
    'GET': C.LCB_HTTP_METHOD_GET,
    'PUT': C.LCB_HTTP_METHOD_PUT,
    'POST': C.LCB_HTTP_METHOD_POST,
    'DELETE': C.LCB_HTTP_METHOD_DELETE
}


class HttpRequest(HttpResult):
    def __init__(self, path, method=C.LCB_HTTP_METHOD_GET,
                 type=C.LCB_HTTP_TYPE_VIEW, response_format=FMT_JSON,
                 content_type='application_json', post_data=None, quiet=False):

        super(HttpRequest, self).__init__()
        self.key = path
        self._parent = None
        self._format = response_format
        self._quiet = quiet
        self._type = type

        if not path:
            raise PyCBC.exc_args('Must provide path')

        def _do_schedule(parent, mres):
            bm = BufManager(ffi)
            cmd = ffi.new('lcb_CMDHTTP*')
            cmd.type = self._type
            cmd.method = method

            C.CBFFI_set_key(cmd, *bm.new_cbuf(path))
            cmd.body, cmd.nbody = bm.new_cbuf(post_data)
            cmd.content_type = bm.new_cstr(content_type)
            rc = C.lcb_http3(parent._lcbh, mres._cdata, cmd)
            if rc:
                raise PyCBC.exc_lcb(rc, 'Scheduling HTTP request')

        self.__sched = _do_schedule

    def _schedule(self, parent, mres):
        mres._quiet = self._quiet
        self._parent = parent
        self.__sched(parent, mres)
        mres[None] = self

    def _handle_response(self, mres, resp):
        result = self
        headers = result.headers

        if resp.headers:
            ix = 0
            while True:
                pp = resp.headers[ix]
                if pp == ffi.NULL:
                    break
                key = from_cstring(resp.headers[ix])
                value = from_cstring(resp.headers[ix+1])
                headers[key] = value
                ix += 2

        result.rc = resp.rc
        result.http_status = resp.htstatus

        if resp.rc:
            mres._add_bad_rc(resp.rc)
        elif not self.success and not mres._quiet:
            try:
                raise PyCBC.exc_http(self.value, response=self)
            except PyCBC.default_exception:
                mres._add_err(sys.exc_info())

        if resp.nbody:
            buf = bytes(ffi.buffer(ffi.cast('const char*', resp.body), resp.nbody))
            tc = self._parent._tc
            try:
                result.value = tc.decode_value(buf, self._format)
            except:
                if not self._quiet:
                    mres._add_err(sys.exc_info())
                result.value = buf


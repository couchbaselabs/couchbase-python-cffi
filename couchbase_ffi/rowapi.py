import sys

from couchbase_ffi.result import HttpResult, AsyncResult
from couchbase_ffi.constants import FMT_JSON, PYCBC_EXC_HTTP
from couchbase_ffi.c import get_handle

ffi, C = get_handle()


class RowResult(HttpResult):
    def __init__(self, parent):
        super(HttpResult, self).__init__()
        self.rows = []
        self.rc = 0
        self.value = None
        self._rows_per_call = 0
        self._parent = parent
        self._format = FMT_JSON

    @classmethod
    def init_with_mres(cls, mres, *args, **kwargs):
        kwargs['mres'] = mres
        mres[None] = cls(*args, **kwargs)
        return mres

    @property
    def _async(self):
        # type: () -> bool
        return self._parent._is_async

    @property
    def _instance(self):
        return self._parent._lcbh

    def _decode(self, value):
        # type: (cdata) -> Any
        return self._parent._tc.decode_value(value, self._format)

    def _should_call(self, is_final):
        if is_final:
            return True
        return -1 < self._rows_per_call < len(self.rows)

    def _invoke_async(self, mres):
        # type: (AsyncResult) -> None
        cb = mres.callback
        if cb:
            cb(mres)
            self.rows = []

    def _step(self, mres, is_last=False):
        # type: (AsyncResult, bool) -> None
        if self._async and self._should_call(is_last):
            self._invoke_async(mres)

        if (not self._async) and self._parent.waiting:
            C.lcb_breakout(self._instance)

    def _done(self, mres, lcb_err, http_status, *_):
        # type: (AsyncResult, int, int, Any) -> None
        self.done = True
        self.http_status = http_status

        if not self.rc:
            self.rc = lcb_err
        if self.rc:
            mres._add_bad_rc(self.rc, self)
        elif http_status != 0 and (http_status > 299 or http_status < 200):
            mres._add_exc_wrap(PYCBC_EXC_HTTP, 'HTTP Request failed', obj=self)

        if self.value:
            try:
                self.value = self._decode(self.value)
            except:
                mres._add_err(sys.exc_info())

        if self._async:
            try:
                mres._maybe_throw()
                self._invoke_async(mres)
            except:
                mres.errback(*sys.exc_info())
            finally:
                del self._parent
        elif not self._parent.waiting:
            C.lcb_breakout(self._instance)

    def fetch(self, mres):
        C.lcb_wait(self._instance)
        ret = self.rows
        self.rows = []
        mres._maybe_throw()
        return ret
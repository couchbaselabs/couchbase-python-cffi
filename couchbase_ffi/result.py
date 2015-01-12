import sys

from couchbase_ffi.constants import (
    PYCBC_RESFLD_CAS, PYCBC_RESFLD_KEY, PYCBC_RESFLD_VALUE,
    PYCBC_RESFLD_HTCODE, PYCBC_RESFLD_URL)

from couchbase_ffi._cinit import get_handle
from couchbase_ffi._rtconfig import PyCBC, pycbc_exc_lcb
from couchbase_ffi._strutil import from_cstring

"""
This file contains the pure-python implementation of the results structures
"""

ffi, C = get_handle()


class Result(object):
    # __slots__ = ['key', 'rc']
    _fldprops = PYCBC_RESFLD_KEY

    @property
    def success(self):
        return self.rc == 0

    @property
    def errstr(self):
        return from_cstring(C.lcb_strerror(ffi.NULL, self.rc))

    def __repr__(self):
        return PyCBC.result_reprfunc(self)


class OperationResult(Result):
    # __slots__ = ['cas']
    _fldprops = PYCBC_RESFLD_KEY | PYCBC_RESFLD_CAS

    def __init__(self):
        self.cas = 0


class ValueResult(OperationResult):
    # __slots__ = ['value', 'flags']
    _fldprops = (PYCBC_RESFLD_KEY | PYCBC_RESFLD_CAS | PYCBC_RESFLD_VALUE)

    def __init__(self):
        super(ValueResult, self).__init__()
        self.value = None
        self.flags = 0


class Item(ValueResult):
    def __getattr__(self, item):
        # This is needed because in C we just check the C field; however
        # in Python, our own __init__ function may not have been called
        if item in ('flags', 'cas', 'rc'):
            return 0


class ObserveInfo(object):
    __slots__ = ['cas', 'flags', 'from_master']

    def __init__(self):
        self.cas = 0
        self.flags = 0
        self.from_master = False

    def __repr__(self):
        return PyCBC.obsinfo_reprfunc(self)


class HttpResult(Result):
    __slots__ = ['htcode', 'headers', 'done', 'http_data', 'fmt']
    _fldprops = (PYCBC_RESFLD_URL | PYCBC_RESFLD_HTCODE | PYCBC_RESFLD_VALUE)

    def __init__(self):
        super(HttpResult, self).__init__()
        self.htcode = 0
        self.headers = {}
        self.http_data = None

    @property
    def url(self):
        return self.key

    @property
    def value(self):
        return self.http_data

    @property
    def http_status(self):
        return self.htcode

    @property
    def success(self):
        if self.rc:
            return False
        if 300 > self.htcode > 199:
            return True
        if not self.htcode:
            return True
        return False


class MultiResult(dict):
    # __slots__ = ['all_ok', '_err', '_remaining', '_cdata', '__flags', '_dur', '_quiet']

    def __init__(self):
        super(MultiResult, self).__init__()
        self.all_ok = True

        # Private attributes
        self._err = None
        self._remaining = 0
        self._cdata = ffi.new_handle(self)
        self._dur = None
        self._quiet = False
        self._no_format = False
        self._is_single = True

    def _add_err(self, exinfo):
        """
        Sets the error on this MultiResult. Will be ignored if an error is
        already set.
        :param exinfo: Return value from ``sys.exc_info()``
        """
        if self._err:
            return
        self._err = exinfo
        self.all_ok = False

    def _add_bad_rc(self, rc, result):
        """
        Sets an error with a bad return code. Handles 'quiet' logic
        :param rc: The error code
        """
        if not rc:
            return

        self.all_ok = False
        if rc == C.LCB_KEY_ENOENT and self._quiet:
            return

        try:
            raise pycbc_exc_lcb(rc)
        except PyCBC.default_exception as e:
            e.all_results = self
            e.key = result.key
            self._add_err(sys.exc_info())

    def _decr_remaining(self):
        """
        Call when a result is received to decrement the remaining count
        :return: True if there are no more items remaining
        """
        assert self._remaining > 0
        self._remaining -= 1
        if not self._remaining:
            self._cdata = None
            return True

    def _maybe_throw(self):
        """
        Throw any deferred exceptions set via :meth:`_add_err`
        """
        if self._err:
            ex_cls, ex_obj, ex_bt = self._err
            self._err = None
            PyCBC.raise_helper(ex_cls, ex_obj, ex_bt)

    def unwrap_single(self):
        """
        Unwrap the single Result item. Call this from single-operation
        methods to return the actual result
        :return: The actual result
        """
        try:
            return next(self.itervalues())
        except AttributeError:
            return next(iter(self.values()))

    def __hash__(self):
        return id(self)


class AsyncResult(MultiResult):
    pass
from couchbase_ffi._cinit import get_handle

ffi, C = get_handle()

class Result(object):
    __slots__ = ['key', 'rc']

    @property
    def success(self):
        return self.rc == 0

    @property
    def errstr(self):
        return ffi.string(C.lcb_strerror(ffi.NULL, self.rc))

class OperationResult(Result):
    __slots__ = ['cas']
    def __init__(self):
        self.cas = 0

class ValueResult(OperationResult):
    __slots__ = ['value', 'flags']
    def __init__(self):
        super(ValueResult, self).__init__()
        self.value = None
        self.flags = 0

class MultiResult(dict):
    __slots__ = ['all_ok', '_err']
    def __init__(self):
        super(MultiResult, self).__init__()
        self.all_ok = True
        self._err = 0

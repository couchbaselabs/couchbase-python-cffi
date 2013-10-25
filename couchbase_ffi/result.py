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
    __slots__ = ['all_ok', '_err', '_priv']
    def __init__(self):
        super(MultiResult, self).__init__()
        self.all_ok = True
        self._err = 0


class ObserveInfo(object):
    __slots__ = ['cas', 'flags', 'from_master']
    def __init__(self):
        self.cas = 0
        self.flags = 0
        self.from_master = False

class HttpResult(Result):
    __slots__ = ['htcode', 'headers', 'done', 'http_data', 'fmt']
    def __init__(self):
        super(HttpResult, self).__init__()
        self.htcode = 0
        self.headers = {}
        self.done = False
        self.http_data = None
        self.fmt = None

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

        if self.htcode < 300 and self.htcode > 199:
            return True

        if not self.htcode:
            return True

        return False

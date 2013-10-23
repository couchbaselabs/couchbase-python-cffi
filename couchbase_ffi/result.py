class Result(object):
    __slots__ = ['key', 'rc']

    @property
    def success(self):
        return self.rc == 0

class OperationResult(Result):
    __slots__ = ['cas']

class ValueResult(OperationResult):
    __slots__ = ['value', 'flags']

class MultiResult(dict):
    __slots__ = ['all_ok', '_err']
    def __init__(self):
        super(MultiResult, self).__init__()
        self.all_ok = True
        self._err = 0

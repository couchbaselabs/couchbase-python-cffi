import inspect

from couchbase.tests.base import ApiImplementationMixin, SkipTest
from couchbase.tests.importer import get_configured_classes

from couchbase_ffi.connection import Connection
from couchbase_ffi.result import (
    MultiResult, OperationResult, Result, ValueResult, ObserveInfo)

class ConfigMixin(ApiImplementationMixin):
    factory = Connection
    should_check_refcount = False
    cls_MultiResult = MultiResult
    cls_ValueResult = ValueResult
    cls_OperationResult = OperationResult
    cls_Result = Result
    cls_ObserveInfo = ObserveInfo

configured_classes = get_configured_classes(ConfigMixin, implstr='_FFI')
globals().update(configured_classes)


# These are not yet implemented via cffi

SKIP_NYI = (
    ConnectionPipelineTest_FFI,
    ConnectionReplicaGetTest_FFI,
    ConnectionItemTest_FFI,
    ConverertSetTest_FFI,
    LockmodeTest_FFI
)

for cls in SKIP_NYI:
    def _setup(*args):
        raise SkipTest("Not Implemented via FFI")
    def _teardown(*args):
        pass
    cls.setUp = _setup
    cls.tearDown = _teardown


SKIP_NOT_SUPPORTED = (
    ConnectionIopsTest_FFI,
)

for cls in SKIP_NOT_SUPPORTED:
    def _setup(*args):
        raise SkipTest("Not supported in FFI mode")
    def _teardown(*args):
        pass
    cls.setUp = _setup
    cls.tearDown = _teardown

def do_skip_tmeth(cls, name):
    def meth(*args):
        raise SkipTest("Not supported in FFI mode")

    setattr(cls, name, meth)


for n in (
    'test_connection_defaults', # Different defaults
    'test_cntl', # Crashes, need wrapper
    'test_newer_ctls', # Crashes, need wrapper
    'test_vbmap', # Crashes, need wrapper
    ):
    do_skip_tmeth(ConnectionMiscTest_FFI, n)

for k, t in inspect.getmembers(ViewIteratorTest_FFI):
    if 'streaming' in k:
        def fn(*args):
            raise SkipTest("Streaming view not supported in FFI")
        setattr(ViewIteratorTest_FFI, k, fn)

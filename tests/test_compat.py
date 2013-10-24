from couchbase.tests.base import ApiImplementationMixin, SkipTest
from couchbase.tests.importer import get_configured_classes

from couchbase_ffi.connection import Connection
from couchbase_ffi.result import (
    MultiResult, OperationResult, Result, ValueResult)

class ConfigMixin(ApiImplementationMixin):
    factory = Connection
    should_check_refcount = False
    cls_MultiResult = MultiResult
    cls_ValueResult = ValueResult
    cls_OperationResult = OperationResult
    cls_Result = Result

configured_classes = get_configured_classes(ConfigMixin, implstr='_FFI')
globals().update(configured_classes)


# These are not yet implemented via cffi

SKIP_NYI = (
    ConnectionEndureTest_FFI,
    ConnectionPipelineTest_FFI,
    ConnectionObserveTest_FFI,
    ConnectionReplicaGetTest_FFI,
    ConnectionStatsDetailTest_FFI,
    ConnectionStatsTest_FFI,
    ConnectionItemTest_FFI,
    ConnectionViewTest_FFI,
    ConverertSetTest_FFI,
    DesignDocManagementTest_FFI
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

# Defaults may be different because of GIL handling
ConnectionMiscTest_FFI.test_connection_defaults = lambda x: None

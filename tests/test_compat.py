import inspect
import couchbase_ffi
from couchbase_ffi.result import MultiResult
from couchbase.tests.base import ApiImplementationMixin, SkipTest
from couchbase.tests.importer import get_configured_classes
from couchbase.bucket import Bucket


class ConfigMixin(ApiImplementationMixin):
    factory = Bucket
    should_check_refcount = False
    cls_MultiResult = MultiResult


configured_classes = get_configured_classes(ConfigMixin, implstr='_FFI')
globals().update(configured_classes)


# These are not yet implemented via cffi

SKIP_NYI = (
    # ConnectionPipelineTest_FFI,
    # ConnectionItemTest_FFI,
    # LockmodeTest_FFI
)

for cls in SKIP_NYI:
    def _setup(*args):
        raise SkipTest("Not Implemented via FFI")
    def _teardown(*args):
        pass
    cls.setUp = _setup
    cls.tearDown = _teardown


SKIP_NOT_SUPPORTED = ()
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
    do_skip_tmeth(MiscTest_FFI, n)

for n in ('test_iterclass',):
    do_skip_tmeth(ItertypeTest_FFI, n)

for n in ('test_subclass_descriptors',):
    do_skip_tmeth(ItemTest_FFI, n)


import sys

if 'couchbase._libcouchbase' in sys.modules:
    raise Exception('The couchbase_ffi module must be imported first!')


def _mk_imp_override(srcname, replacement):
    """
    Create a simple one for one replacement for a module
    :param srcname: The source module name to replace
    :param replacement: The object which should act as the replacement
    """
    class DummyImporter(object):
        def find_module(self, fullname, path):
            if fullname == srcname:
                return self

            return None

        def load_module(self, fullname):
            if fullname != srcname:
                raise ImportError
            sys.modules[fullname] = replacement
            return replacement

    obj = DummyImporter()
    sys.meta_path.append(obj)


import couchbase_ffi.constants as constants
_mk_imp_override('couchbase.user_constants', constants)


_libcouchbase = None


class LibcouchbaseModule(object):
    Transcoder = None

    def __getattr__(self, item):
        if _libcouchbase is not None and hasattr(_libcouchbase, item):
            return getattr(_libcouchbase, item)
        if item in globals():
            return globals()[item]
        if hasattr(constants, item):
            return getattr(constants, item)

        raise AttributeError(item)

_mk_imp_override('couchbase._libcouchbase', LibcouchbaseModule())

import couchbase_ffi._libcouchbase as _libcouchbase
_libcouchbase._stage2_bootstrap()
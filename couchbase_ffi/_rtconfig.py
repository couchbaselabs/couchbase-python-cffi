import sys

from couchbase_ffi.constants import (
    PYCBC_EXC_ARGUMENTS,
    PYCBC_EXC_ENCODING,
    PYCBC_EXC_THREADING,
    PYCBC_EXC_PIPELINE,
    PYCBC_EXC_HTTP
)

_IS_INITIALIZED = False

V = sys.version_info[0]

class _PyCBC_Class(object):
    """
    This object represents global helpers which are cumulatively set via the
    couchbase._bootstrap module
    """

    def __init__(self):
        global _IS_INITIALIZED
        if _IS_INITIALIZED:
            raise ValueError(
                'This class cannot be initialized more than once!')

        _IS_INITIALIZED = True
        self.result_reprfunc = None
        self.fmt_utf8_flags = 0
        self.fmt_bytes_flags = 0
        self.fmt_pickle_flags = 0
        self.fmt_json_flags = 0
        self.pickle_encode = None
        self.pickle_decode = None
        self.json_encode = None
        self.json_decode = None
        self.lcb_errno_map = None
        self.misc_errno_map = None
        self.default_exception = None
        self.obsinfo_reprfunc = None
        self.itmcoll_base_type = None
        self.itmopts_dict_type = None
        self.itmopts_seq_type = None
        self.fmt_auto = None
        self.pypy_mres_factory = None
        self.view_path_helper = None

    def configure(self, key, value):
        if not hasattr(self, key):
            raise KeyError('No such key: {0}'.format(key))
        setattr(self, key, value)

    def get(self, key):
        return getattr(self, key)

    def raise_helper(self, cls, obj, bt):
        if V == 2:
            exec('raise cls, obj, bt')
        else:
            raise obj.with_traceback(bt)

    def exc_common(self, mode, msg, rc, **params):
        _, cur_ex, cur_bt = sys.exc_info()
        cls = self.misc_errno_map[mode]
        params['message'] = msg
        params['rc'] = rc
        if cur_ex is not None:
            params['inner_cause'] = cur_ex

        new_ex = cls(params)
        if cur_bt:
            self.raise_helper(cls, new_ex, cur_bt)
        else:
            raise new_ex

    def exc_args(self, msg='Bad arguments provided', obj=None):
        self.exc_common(PYCBC_EXC_ARGUMENTS, msg, 0, objextra=obj)

    def exc_enc(self, msg='Bad key/value encoding', obj=None):
        self.exc_common(PYCBC_EXC_ENCODING, msg, 0, objextra=obj)

    def exc_lcb(self, rc, msg='Operational error'):
        try:
            cls = self.lcb_errno_map[rc]
        except KeyError:
            cls = self.default_exception
        raise cls({'rc': rc, 'message': msg})

    def exc_lock(self, msg=None):
        if msg is None:
            msg = 'LOCKMODE_WAIT not specified and Bucket already locked'
        self.exc_common(PYCBC_EXC_THREADING, msg, 0)

    def exc_pipeline(self, msg):
        self.exc_common(PYCBC_EXC_PIPELINE, msg, 0)

    def exc_http(self, msg='HTTP Error', response=None):
        self.exc_common(PYCBC_EXC_HTTP, msg, 0, objextra=response)


PyCBC = _PyCBC_Class()
pycbc_exc_args = PyCBC.exc_args
pycbc_exc_enc = PyCBC.exc_enc
pycbc_exc_lcb = PyCBC.exc_lcb
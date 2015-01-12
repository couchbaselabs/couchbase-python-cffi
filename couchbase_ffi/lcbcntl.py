from couchbase_ffi._cinit import get_handle
from couchbase_ffi._rtconfig import pycbc_exc_lcb
from couchbase_ffi._strutil import from_cstring

ffi, C = get_handle()


class CntlHandler(object):
    def allocate(self, mode):
        """
        Allocate the pointer. Mode is provided in case input and output allocations differ
        """
        raise NotImplementedError()

    def convert_input(self, py_arg, c_value):
        raise NotImplementedError()

    def convert_output(self, c_value):
        raise NotImplementedError()

    def execute(self, lcbh, op, value):
        if value is not None:
            mode = C.LCB_CNTL_SET
        else:
            mode = C.LCB_CNTL_GET
        c_data = self.allocate(mode)

        if mode == C.LCB_CNTL_SET:
            self.convert_input(value, c_data)
            rc = C.lcb_cntl(lcbh, mode, op, c_data)
        else:
            rc = C.lcb_cntl(lcbh, mode, op, c_data)
            if not rc:
                return self.convert_output(c_data)
        if rc:
            raise pycbc_exc_lcb(rc)


class TimeoutHandler(CntlHandler):
    def allocate(self, mode):
        return ffi.new('lcb_U32*')

    def convert_input(self, py_arg, c_value):
        f_val = py_arg * 1000000
        c_value[0] = int(f_val)

    def convert_output(self, c_value):
        return float(c_value[0]) / 1000000


class SimpleAssignHandler(CntlHandler):
    def convert_input(self, py_arg, c_value):
        c_value[0] = py_arg

    def convert_output(self, c_value):
        return c_value[0]


class IntHandler(SimpleAssignHandler):
    def allocate(self, mode):
        return ffi.new('int*')


class UIntHandler(SimpleAssignHandler):
    def allocate(self, mode):
        return ffi.new('unsigned*')


class SizeHandler(SimpleAssignHandler):
    def allocate(self, mode):
        return ffi.new('size_t*')


class FloatHandler(SimpleAssignHandler):
    def allocate(self, mode):
        return ffi.new('float*')


class U32Handler(SimpleAssignHandler):
    def allocate(self, mode):
        return ffi.new('lcb_U32*')


class StringHandler(CntlHandler):
    def allocate(self, mode):
        return ffi.new('char **')

    def convert_input(self, py_arg, c_value):
        c_value[0] = py_arg

    def convert_output(self, c_value):
        return from_cstring(c_value[0])


CNTL_VTYPE_MAP = {
    'str': StringHandler(),
    'string': StringHandler(),
    'timeout': TimeoutHandler(),
    'int': IntHandler(),
    'uint': UIntHandler(),
    'unsigned': UIntHandler(),
    'size_t': SizeHandler(),
    'lcb_size_t': SizeHandler(),
    'float': FloatHandler(),
    'uint32_t': U32Handler(),
    'lcb_uint32_t': U32Handler()
}


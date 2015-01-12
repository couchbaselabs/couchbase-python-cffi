"""
Module to help with creation and mapping of C buffers to python buffers
"""


class BufManager(object):
    """
    Buffer manager which transparently maintains backing C buffers in
    its object, so that it doesn't go out of scope. This allows
    convenient assignment to C structures without explicitly
    creating an intermediate variable.
    """
    def __init__(self, ffi):
        self._ffi = ffi
        self._cache = {}
        self._bufs = []

    def new_cstr(self, input, null_if_empty=True):
        """
        Converts the input into an encoded C String (NUL-terminated)
        :param input: The python string
        :param null_if_empty: If the input is empty, return NULL rather
            than the empty string
        :return: The C string
        """
        if input:
            enc = input.encode('utf-8')
        else:
            enc = ''.encode('utf-8')
        if not enc:
            if null_if_empty:
                return self._ffi.NULL
        try:
            return self._cache[enc]
        except KeyError:
            cstr = self._ffi.new('char[]', enc)
            self._cache[enc] = cstr
            return cstr

    def new_cbuf(self, input, null_if_empty=True):
        """
        Converts the input into a raw C buffer
        :param input: The input
        :param null_if_empty: If the input is empty
        :return: A tuple of buffer,length
        """
        if not isinstance(input, bytes) and input:
            input = input.encode('utf-8')
        if not input and null_if_empty:
            return self._ffi.NULL, 0

        cbuf = self._ffi.new('char[]', input)
        self._bufs.append(cbuf)
        return cbuf, len(input)
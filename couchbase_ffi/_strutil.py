from couchbase_ffi.c import get_handle
from sys import version_info


V = version_info[0]
ffi, C = get_handle()

def from_cstring(cs, n=-1):
    s = ffi.string(cs, n)
    if V == 3:
        return s.decode('utf-8')
    else:
        return s
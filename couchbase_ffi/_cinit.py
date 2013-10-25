import os.path
import subprocess
from cffi import FFI

ffi = FFI()
C = None

CPP_INPUT=b"""
#define LIBCOUCHBASE_COUCHBASE_H
#define LIBCOUCHBASE_API

typedef int64_t lcb_int64_t;
typedef int32_t lcb_int32_t;
typedef size_t lcb_size_t;
typedef ssize_t lcb_ssize_t;
typedef uint16_t lcb_vbucket_t;
typedef uint8_t lcb_uint8_t;
typedef uint16_t lcb_uint16_t;
typedef uint32_t lcb_uint32_t;
typedef uint64_t lcb_cas_t;
typedef uint64_t lcb_uint64_t;
typedef unsigned long lcb_time_t;
#include <libcouchbase/error.h>
#include <libcouchbase/types.h>
#include <libcouchbase/http.h>
#include <libcouchbase/arguments.h>
#include <libcouchbase/durability.h>
#include <libcouchbase/callbacks.h>

const char *
lcb_strerror(lcb_t, lcb_error_t);

lcb_error_t
lcb_create(lcb_t*, struct lcb_create_st *);

lcb_error_t
lcb_wait(lcb_t);

lcb_error_t
lcb_store(lcb_t, const void *,  lcb_size_t, const lcb_store_cmd_t **);

lcb_error_t
lcb_get(lcb_t, const void *, lcb_size_t, const lcb_get_cmd_t **);

lcb_error_t
lcb_touch(lcb_t, const void *, lcb_size_t, const lcb_touch_cmd_t **);

lcb_error_t
lcb_remove(lcb_t, const void *, lcb_size_t, const lcb_remove_cmd_t **);

lcb_error_t
lcb_unlock(lcb_t, const void *, lcb_size_t, const lcb_unlock_cmd_t **);

lcb_error_t
lcb_arithmetic(lcb_t, const void *, lcb_size_t, const lcb_arithmetic_cmd_t **);

lcb_error_t
lcb_server_stats(lcb_t, const void *, lcb_size_t, const lcb_server_stats_cmd_t **);

lcb_error_t
lcb_observe(lcb_t, const void *, lcb_size_t, const lcb_observe_cmd_t **);

lcb_error_t
lcb_make_http_request(lcb_t, const void *, lcb_http_type_t,
                      const lcb_http_cmd_t *, lcb_http_request_t*);

lcb_error_t
lcb_durability_poll(lcb_t, const void *, const lcb_durability_opts_t *,
                    lcb_size_t, const lcb_durability_cmd_t **);

lcb_int32_t lcb_get_num_replicas(lcb_t);
"""

VERIFY_INPUT=b"""
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <libcouchbase/couchbase.h>
"""

CPP_OUTPUT = os.path.join(os.path.dirname(__file__), "_lcb.h")

LCB_ROOT = '/sources/libcouchbase/inst/'

def _exec_cpp():
    po = subprocess.Popen((
        'cpp', '-E', '-Wall', '-Wextra',
        '-I{0}/include'.format(LCB_ROOT),
        '-xc',
        '-std=c89',
        '-',
    ), stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    stdout, _ = po.communicate(CPP_INPUT)
    try:
        lines = str(stdout, "utf8").split("\n")
    except TypeError:
        lines = stdout.split("\n")

    outlines = []
    for l in lines:
        if l.startswith('#'):
            continue
        if not l:
            continue

        outlines.append(l)

    with open(CPP_OUTPUT, "w") as fp:
        fp.write("\n".join(outlines))


def get_handle():
    global C
    if C:
        return (ffi, C)

    _exec_cpp()
    ffi.cdef(open(CPP_OUTPUT, "r").read())
    C = ffi.verify(VERIFY_INPUT,
                   libraries=['couchbase'],
                   library_dirs=[os.path.join(LCB_ROOT, 'lib')],
                   include_dirs=[os.path.join(LCB_ROOT, 'include')],
                   runtime_library_dirs=[os.path.join(LCB_ROOT, 'lib')])

    return (ffi, C)


CALLBACK_DECLS = {
    'store':
        'void(lcb_t,const void*,lcb_storage_t,lcb_error_t,const lcb_store_resp_t*)',
    'get':
        'void(lcb_t,const void*,lcb_error_t,const lcb_get_resp_t*)',
    'delete':
        'void(lcb_t,const void*,lcb_error_t,const lcb_remove_resp_t*)',
    'arith':
        'void(lcb_t,const void*,lcb_error_t,const lcb_arithmetic_resp_t*)',
    'error':
        'void(lcb_t,lcb_error_t,const char*)',
    'touch':
        'void(lcb_t,const void*,lcb_error_t,const lcb_touch_resp_t*)',
    'unlock':
        'void(lcb_t,const void*,lcb_error_t,const lcb_unlock_resp_t*)',
    'observe':
        'void(lcb_t,const void*,lcb_error_t,const lcb_observe_resp_t*)',
    'stats':
        'void(lcb_t,const void*,lcb_error_t,const lcb_server_stat_resp_t*)',
    'http':
        'void(lcb_http_request_t,lcb_t,const void*,lcb_error_t,const lcb_http_resp_t*)',
    'endure':
        'void(lcb_t,const void*,lcb_error_t,const lcb_durability_resp_t*)'
}

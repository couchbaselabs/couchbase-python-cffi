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
typedef int lcb_http_method_t;
typedef int lcb_http_status_t;
#include <libcouchbase/error.h>
#include <libcouchbase/types.h>
#include <libcouchbase/arguments.h>
#include <libcouchbase/durability.h>
#include <libcouchbase/callbacks.h>

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
"""

VERIFY_INPUT=b"""
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <libcouchbase/couchbase.h>
"""

CPP_OUTPUT = os.path.join(os.path.dirname(__file__), "_lcb.h")

def _exec_cpp():
    po = subprocess.Popen((
        'cpp', '-E', '-Wall', '-Wextra',
        '-I/sources/libcouchbase/inst/include',
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
                   library_dirs=['/sources/libcouchbase/inst/lib'],
                   include_dirs=['/sources/libcouchbase/inst/include'])

    return (ffi, C)

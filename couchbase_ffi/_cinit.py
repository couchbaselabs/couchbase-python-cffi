from __future__ import print_function
import os
import subprocess
import re

from cffi import FFI

# Globals
CPP_OUTPUT = os.path.join(os.path.dirname(__file__), "_lcb.h")
FAKE_INKPATH = os.path.join(os.path.dirname(__file__), 'fakeinc')
LCB_ROOT = os.environ.get('PYCBC_CFFI_PREFIX', '')

ffi = FFI()
C = None

CPP_INPUT = """
#define __attribute__(x)
#include <libcouchbase/couchbase.h>
#include <libcouchbase/api3.h>
#include <libcouchbase/views.h>
#include <libcouchbase/n1ql.h>

void _Cb_set_key(void*,const void*, size_t);
void _Cb_set_val(void*,const void*, size_t);
void _Cb_do_callback(lcb_socket_t s, short events, lcb_ioE_callback cb, void *arg);
void memset(void*,int,int);
"""

VERIFY_INPUT = """
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <libcouchbase/couchbase.h>
#include <libcouchbase/api3.h>
#include <libcouchbase/views.h>
#include <libcouchbase/n1ql.h>

void _Cb_set_key(void *cmd, const void *key, size_t nkey) {
    LCB_CMD_SET_KEY((lcb_CMDBASE*)cmd, key, nkey);
}
void _Cb_set_val(void *cmd, const void *val, size_t nval) {
    LCB_CMD_SET_VALUE((lcb_CMDSTORE*)cmd, val, nval);
}
void _Cb_do_callback(lcb_socket_t s, short events, lcb_ioE_callback cb, void *arg) {
    cb(s, events, arg);
}
"""

RX_SHIFT = re.compile(r'(\(?\d+\)?)\s*((?:<<)|(?:>>)|(?:\|))\s*(\(?\d+\)?)')


def shift_replace(m):
    ss = '{0} {1} {2}'.format(m.group(1), m.group(2), m.group(3))
    return str(eval(ss))


def do_replace_vals(dh, decl):
    keys = sorted(dh, cmp=lambda x, y: cmp(len(x), len(y)), reverse=True)
    for k in keys:
        decl = decl.replace(k, str(dh[k]))
    return decl


def handle_enumvals(defhash, linedecl):
    # First, inspect to see if there is any funky magic going on here,
    # this can include things like shifts and the like
    linedecl = linedecl.strip()
    cur_decls = []

    for decl in linedecl.split(','):
        if not decl:
            continue
        if not '=' in decl:
            cur_decls.append(decl)
            continue

        if '{' in decl:
            preamble, decl = decl.split('{')
            preamble += "{"
        else:
            preamble = ""

        if '}' in decl:
            decl, postamble = decl.split('}')
            postamble = "}" + postamble
        else:
            postamble = ""

        print(decl)
        name, val = decl.split('=', 1)
        name = name.strip()
        val = val.strip()
        val = val.replace(',', '')
        val = do_replace_vals(defhash, val)

        if not name.lower().startswith('lcb'):

            continue

        print("Handling", decl)
        while RX_SHIFT.search(val):
            val = RX_SHIFT.sub(shift_replace, val)

        try:
            ival = int(val)
        except ValueError:
            ival = int(val, 16)

        decl = '{0}={1}'.format(name, str(ival))
        defhash[name] = ival
        cur_decls.append(preamble + decl + postamble)

    ret = ','.join(cur_decls)
    if '}' not in ret:
        ret += ','
    return ret


CPP_COMMON = ['gcc', '-E', '-Wall', '-Wextra',
              '-I{0}'.format(FAKE_INKPATH), '-I{0}/include'.format(LCB_ROOT),
              '-std=c89', '-xc']


def get_preprocessed(csrc, extra_options=None):
    options = CPP_COMMON[::]
    if extra_options:
        options += extra_options
    options += ['-']

    po = subprocess.Popen(options, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = po.communicate(csrc)
    if po.returncode != 0:
        raise ValueError("Bad CPP Input!")

    try:
        return str(stdout, 'utf8').split("\n")
    except TypeError:
        return stdout.split("\n")


def _exec_cpp():
    lines = get_preprocessed(CPP_INPUT)
    outlines = []
    defhash = {}

    for l in lines:
        if l.startswith('#'):
            continue
        if not l:
            continue

        # Find definitions
        if '=' in l and '==' not in l:
            # Handle enums
            l = handle_enumvals(defhash, l)

        l = l.replace("\r", "")

        outlines.append(l)

    with open(CPP_OUTPUT, "w") as fp:
        fp.write("\n".join(outlines))
        fp.flush()


def ensure_header():
    if os.environ.get('PYCBC_CFFI_REGENERATE'):
        do_generate = True
    elif not os.path.exists(CPP_OUTPUT):
        do_generate = True
    else:
        do_generate = False

    if do_generate:
        _exec_cpp()


def get_handle():
    global C
    if C:
        return ffi, C

    ensure_header()

    ffi.cdef(open(CPP_OUTPUT, "r").read())
    ffi.cdef(r'''
#define LCB_CMDOBSERVE_F_MASTER_ONLY ...
#define LCB_RESP_F_FINAL ...
#define LCB_CNTL_SET ...
#define LCB_CNTL_GET ...
#define LCB_CNTL_BUCKETNAME ...
#define LCB_CNTL_VBMAP ...
#define LCB_CMDVIEWQUERY_F_INCLUDE_DOCS ...
#define LCB_N1P_QUERY_STATEMENT ...
''')

    C = ffi.verify(VERIFY_INPUT,
                   libraries=['couchbase'],
                   library_dirs=[os.path.join(LCB_ROOT, 'lib')],
                   include_dirs=[os.path.join(LCB_ROOT, 'include')],
                   runtime_library_dirs=[os.path.join(LCB_ROOT, 'lib')])

    return ffi, C

import os.path
import os
import subprocess
import re
from cffi import FFI

ffi = FFI()
C = None

CPP_INPUT=b"""
#define __attribute__(x)
#include <libcouchbase/sysdefs.h>
#include <libcouchbase/couchbase.h>
"""

VERIFY_INPUT=b"""
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <libcouchbase/couchbase.h>
"""

CPP_OUTPUT = os.path.join(os.path.dirname(__file__), "_lcb.h")
FAKE_INKPATH = os.path.join(os.path.dirname(__file__), 'fakeinc')
LCB_ROOT = '/sources/libcouchbase/inst/'

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
    has_comma = linedecl.endswith(',')
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

        name, val = decl.split('=', 1)
        name = name.strip()
        val = val.strip()
        val = val.replace(',', '')
        val = do_replace_vals(defhash, val)

        if not name.lower().startswith('lcb'):

            continue

        print "Handling", decl
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
    if not '}' in ret:
        ret += ','
    return ret




def _exec_cpp():

    if not os.environ.get('PYCBC_GENHEADER'):
        return

    cpp_cmd = ('gcc', '-E', '-Wall', '-Wextra',
               '-I{0}'.format(FAKE_INKPATH),
               '-I{0}/include'.format(LCB_ROOT),
               '-std=c89',
               '-xc', '-')

    rx_shifty = re.compile(r'([^=]+)=.*(?:(?:<<)|(?:>>)|(?:\|))[^,]+')
    po = subprocess.Popen(cpp_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    stdout, _ = po.communicate(CPP_INPUT)
    try:
        lines = str(stdout, "utf8").split("\n")
    except TypeError:
        lines = stdout.split("\n")

    outlines = []
    defhash = {}

    for l in lines:
        if l.startswith('#'):
            continue
        if not l:
            continue

        # Find definitions
        if '=' in l and '==' not in l: # Enums!
            l = handle_enumvals(defhash, l)

        l = l.replace("\r", "")

        outlines.append(l)

    with open(CPP_OUTPUT, "w") as fp:
        fp.write("\n".join(outlines))
        fp.flush()


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

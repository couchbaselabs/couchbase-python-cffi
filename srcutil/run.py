#!/usr/bin/env python
import sys
import imp

if len(sys.argv) < 2:
    print "Usage: {0} SCRIPT ARGS".format(sys.argv[0])
    print "  Ensure both the couchbase and couchbase_ffi are findable by Python"
    sys.exit(1)

import couchbase_ffi

sys.argv.pop(0)
imp.load_source('__main__', sys.argv[0])

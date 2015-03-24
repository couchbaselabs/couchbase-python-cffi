#!/usr/bin/env python
# This simple script will simply dump the constants of the currently installed
# 'couchbase' module.
import couchbase

couchbase._libcouchbase.dump_constants()

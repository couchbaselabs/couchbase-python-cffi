=============
Couchbase FFI
=============

.. image:: https://travis-ci.org/couchbaselabs/couchbase-python-cffi.png
    :target: https://travis-ci.org/couchbaselabs/couchbase-python-cffi

This provides the FFI backend for the
`couchbase <http://github.com/couchbase/couchbase-python-client>`_ module. This
project is mainly of use to those who wish to use the couchbase module with
`pypy`. Normal CPython extensions do not work very well on pypy, and thus
the recommended way of interfacing via `pypy` in a C library is to use the
`cffi` module.

Using
-----

**WARNING** - This module still depends on un-merged features in both
*libcouchbase* and the *couchbase* proejcts. This means the
module will likely not work yet. Please use the master branch.

You will need the `cffi` Python module (the newer, the better), the libcouchbase
development files, and the actual `couchbase` module (see its instructions for
how to build it).

Once you've built all that, you must load this module first before any others;
thus::

    import couchbase_ffi
    from couchbase.bucket import Bucket
    # ...


This module will **inject itself** as the ``couchbase._libcouchbase`` module,
allowing you to use anything that depends on the C extension normally.

This module does *not* monkey-patch the couchbase ``Bucket`` class, but rather
the underlying C internals; therefore the ability of a drop-in increases.

The first time you use the module, the `couchbase_ffi._cinit` module will
attempt to generate the appropriate stubs for the library. Regeneration may
also take place if you have upgraded your libcouchbase installation.

Because regenerating the header might involve some hacks in dynamically
patching the header file to make it acceptable to `pycparser`, it may fail
at times.


Ennvironment variables affecting how the headers are built:

* ``PYCBC_CFFI_REGENERATE`` forces the header to be rebuilt
* ``PYCBC_CFFI_PREFIX`` sets the installation prefix for libcouchbase


Implemented Features
--------------------

Everything the normal C extension supports. This has been tested using the
normal `couchbase.tests` module *and* the twisted tests.

I may have missed something here and there, but I can't think of anything
that isn't supported.

TODO
----

Better tests.

Performance
-----------

Here are some examples using the ``bench.py`` script in the main Couchbase
Python distribution.

==============  =======  =======
--------------  -------  -------
Implementation  Threads  Ops/Sec
==============  =======  =======
FFI (PyPy)      0        8200
FFI (CPython)   0        4500
Ext (PyPy)      0        4800
Ext (CPython)   0        11200
FFI (PyPy)      4        15300
FFI (CPython)   4        4600
Ext (PyPy)      4        4400
Ext (CPython)   4        27000
==============  =======  =======


For twisted:

==============  =======  =======
--------------  -------  -------
Implementation  C/T      Ops/Sec
==============  =======  =======
FFI (PyPy)      1/1      5850
FFI (CPython)   1/1      2600
Ext (CPython)   1/1      5950
FFI (PyPy)      4/4      26000
FFI (CPython)   4/4      7500
Ext (CPython)   4/4      33600
FFI (PyPy)      10/10    32557
FFI (CPython)   10/10    9290
Ext (CPython)   10/10    42160
==============  =======  =======


The *T* and *C* values show how many total clients were spawned, and how many
independent logical sequences (threads) of operations were being performed.
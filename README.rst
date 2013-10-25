=============
Couchbase FFI
=============

This project aims to supplant much of the Couchbase Python SDK functionality
with variants written in Python. Interactions with libcouchbase will still be
performed using `cffi`

This project is mainly of use to PyPy, as this performs quicker (and is more
stable) than the C extension using PyPy's `cpyext` layer. For CPython this
module is rather slow and should not be used (though there is no reason why it
should not work).

This aims to be a drop-in replacement for the `couchbase` module, though it
currently depends on it for some other routines (mainly some of the module
and object structure which has not yet been re-implemented).


Using
-----

Currently I don't know how to make a proper ``setup.py`` for a ``cffi``-based
project.

You will need the ``couchbase``
(https://github.com/couchbase/couchbase-python-client) installed. This will
also assume you have libcouchbase, its headers. After that, simply use the
``couchbase_ffi.connection.Connection`` class as you would the
``couchbase.connection.Connection`` class.

TODO
----

The following features have not yet been implemented. They are planned:

* Durability
* Replica reads
* ``streaming`` option with Views
* Context Managers
* Threading

Twisted and gevent support will never be supported by this module.

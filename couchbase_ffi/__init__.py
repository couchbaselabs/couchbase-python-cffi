from couchbase_ffi.connection import Connection

class CouchbaseFFI(object):
    @classmethod
    def connect(self, **kwargs):
        return Connection(**kwargs)

Couchbase = CouchbaseFFI

from couchbase.transcoder import TranscoderPP
from couchbase.connection import Connection as _ExtConnection
from couchbase.user_constants import *
from couchbase.exceptions import CouchbaseError, ValueFormatError

from couchbase_ffi._cinit import get_handle
from couchbase_ffi.result import (MultiResult, OperationResult, ValueResult)
from couchbase_ffi.context import (
    CommandContext,
    GetCommandContext,
    StoreCommandContext,
    RemoveCommandContext,
    Options
)

import couchbase_ffi.context

ffi, C = get_handle()

couchbase_ffi.context.ffi = ffi
couchbase_ffi.context.C = C

CALLBACK_DECLS = {
    'store':
        'void(lcb_t,const void*,lcb_storage_t,lcb_error_t,const lcb_store_resp_t*)',
    'get':
        'void(lcb_t,const void*,lcb_error_t,const lcb_get_resp_t*)',
    'delete':
        'void(lcb_t,const void*,lcb_error_t,const lcb_remove_resp_t*)'
}


def _shadow_prop(name):
    def x_get(self):
        return self._shadow_props[name]

    def x_set(self, val):
        #_ExtConnection.__setattr__(self, name, val)
        self._shadow_props[name] = val

    return property(x_get, x_set)

class Connection(_ExtConnection):
    quiet = _shadow_prop('quiet')
    default_format = _shadow_prop('default_format')
    transcoder = _shadow_prop('transcoder')

    @property
    def _tc(self):
        return self.transcoder

    def __init__(self, **kwargs):
        self._shadow_props = {
            'quiet': None,
            'default_format': FMT_JSON,
            'transcoder': None,
        }

        super(Connection, self).__init__(**kwargs)
        self._instance = ffi.cast('lcb_t', self._instance_pointer)

        self._bound_cb = {
            'store': ffi.callback(CALLBACK_DECLS['store'],
                                  self._storage_callback),
            'get': ffi.callback(CALLBACK_DECLS['get'],
                                self._get_callback),
            'remove': ffi.callback(CALLBACK_DECLS['delete'],
                                   self._opres_callback)
        }

        C.lcb_set_store_callback(self._instance, self._bound_cb['store'])
        C.lcb_set_get_callback(self._instance, self._bound_cb['get'])
        C.lcb_set_remove_callback(self._instance, self._bound_cb['remove'])

        self._cur_op = None
        self.transcoder = TranscoderPP()

    def _get_response_key(self, resp):
        key = ffi.buffer(resp.v.v0.key, resp.v.v0.nkey)[:]
        key = self._tc.decode_key(key)
        return key

    def _add_response(self, cres, pres):
        key = self._get_response_key(cres)
        self._cur_op[key] = pres
        if not pres.success:
            if pres.rc == C.LCB_KEY_ENOENT and  (self._cur_ctx.quiet or self.quiet):
                return

            if not self._cur_op._err:
                self._cur_op._err = pres.rc

            self._cur_op.all_ok = False

    def _opres_callback(self, instance, cookie, err, resp):
        res = OperationResult()
        res.cas = resp.v.v0.cas
        res.rc = err
        self._add_response(resp, res)


    def _storage_callback(self, instance, cookie, op, err, resp):
        self._opres_callback(instance, cookie, err, resp)

    def _get_callback(self, instance, cookie, err, resp):
        res = ValueResult()
        res.cas = resp.v.v0.cas
        res.flags = resp.v.v0.flags
        res.rc = err

        if not err:
            value = ffi.buffer(resp.v.v0.bytes, resp.v.v0.nbytes)[:]
            value = self._tc.decode_value(value, resp.v.v0.flags)
            res.value = value

        self._add_response(resp, res)

    def _maybe_raise(self, err):
        if not err:
            return

        excls = CouchbaseError.rc_to_exctype(err)
        raise excls.pyexc()

    def _invoke_common(self, fn, ctx, is_multi):
        err = fn(self._instance, ffi.NULL, *ctx.args())
        self._maybe_raise(err)

        self._cur_op = MultiResult()
        self._cur_ctx = ctx

        C.lcb_wait(self._instance)

        if not self._cur_op.all_ok:
            self._maybe_raise(self._cur_op._err)

        if is_multi:
            return self._cur_op
        return self._cur_op.values()[0]

    def _invoke_single_storage(self, mode, key, value, **kwargs):
        ctx = StoreCommandContext(self, mode, {key:value}, **kwargs)
        return self._invoke_common(C.lcb_store, ctx, False)

    def _invoke_multi_storage(self, mode, kv, **kwargs):
        ctx = StoreCommandContext(self, mode, kv, **kwargs)
        return self._invoke_common(C.lcb_store, ctx, True)

    def set(self, key, value, **kwargs):
        return self._invoke_single_storage(C.LCB_SET, key, value, **kwargs)

    def add(self, key, value, **kwargs):
        return self._invoke_single_storage(C.LCB_ADD, key, value, **kwargs)

    def replace(self, key, value, **kwargs):
        return self._invoke_single_storage(C.LCB_REPLACE, key, value, **kwargs)

    def append(self, key, value, **kwargs):
        return self._invoke_single_storage(C.LCB_APPEND, key, value, **kwargs)

    def prepend(self, key, value, **kwargs):
        return self._invoke_single_storage(C.LCB_PREPEND, key, value, **kwargs)

    def get(self, key, **kwargs):
        ctx = GetCommandContext(self, (key,), **kwargs)
        return self._invoke_common(C.lcb_get, ctx, False)

    def set_multi(self, kv, **kwargs):
        return self._invoke_multi_storage(C.LCB_SET, kv, **kwargs)

    def add_multi(self, kv, **kwargs):
        return self._invoke_multi_storage(C.LCB_ADD, kv, **kwargs)

    def replace_multi(self, kv, **kwargs):
        return self._invoke_multi_storage(C.LCB_REPLACE, kv, **kwargs)

    def append_multi(self, kv, **kwargs):
        return self._invoke_multi_storage(C.LCB_APPEND, kv, **kwargs)

    def prepend_multi(self, kv, **kwargs):
        return self._invoke_multi_storage(C.LCB_PREPEND, kv, **kwargs)

    def get_multi(self, keys, **kwargs):
        ctx = GetCommandContext(self, keys, **kwargs)
        return self._invoke_common(C.lcb_get, ctx, True)

    def delete(self, key, **kwargs):
        ctx = RemoveCommandContext(self, (key,), **kwargs)
        return self._invoke_common(C.lcb_remove, ctx, False)

    def delete_multi(self, kv, **kwargs):
        ctx = RemoveCommandContext(self, kv, **kwargs)
        return self._invoke_common(C.lcb_remove, ctx, True)

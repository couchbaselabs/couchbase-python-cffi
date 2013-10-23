from couchbase.exceptions import ValueFormatError, ArgumentError
from couchbase.user_constants import *

ffi = None
C = None

class Options(dict):
    pass

class CommandContext(object):
    def __init__(self, conn, structname, **kwargs):
        self._basename = structname
        self._conn = conn

        self.quiet = kwargs.get('quiet', False)

    def make_struct_pointers(self, ncmds):
        fmtstr_l = "{0} [{1}]"
        fmtstr_pp = "{0} *[{1}]"

        self._cmdlist = ffi.new(fmtstr_l.format(self._basename, ncmds))
        self._cmdpp = ffi.new(fmtstr_pp.format(self._basename, ncmds))
        self._cdata = []
        self._ncmds = ncmds

    def process_single_command(self, req, koptions):
        raise NotImplentedError()

    def _build_single(self, kv, kviter, ix):
        try:
            cur = kviter.next()
        except AttributeError:
            cur = kviter.__next__()

        if isinstance(kv, dict):
            key, koptions = cur

        else:
            key = cur
            koptions = Options()

        cmd = self._cmdlist[ix]
        self._cmdpp[ix] = ffi.addressof(cmd)

        k_enc = self._conn._tc.encode_key(key)
        s_key = ffi.new('char[]', k_enc)
        self._cdata.append(s_key)

        req = cmd.v.v0
        req.key = s_key
        req.nkey = len(k_enc)

        self.process_single_command(req, koptions)

    def build(self, kv):
        self.make_struct_pointers(len(kv))
        curix = 0

        if isinstance(kv, dict):
            kviter = kv.iteritems()
        else:
            kviter = iter(kv)

        while True:
            try:
                self._build_single(kv, kviter, curix)
                curix += 1

            except StopIteration:
                break

        return self._cmdpp

    def args(self):
        return (self._ncmds, self._cmdpp)


class StoreCommandContext(CommandContext):
    def __init__(self, parent, mode, kv, cas=0, ttl=0, format=None, **kwargs):
        super(StoreCommandContext, self).__init__(parent,
                                                  'lcb_store_cmd_t',
                                                  **kwargs)

        if format is None:
            if mode in (C.LCB_APPEND, C.LCB_PREPEND):
                format = FMT_UTF8
            else:
                format = parent.default_format

        self._koptions = Options({
            'cas': cas,
            'ttl': ttl,
            'format': format
        })

        self._mode = mode
        self.build(kv)

    def process_single_command(self, req, koptions):
        if not isinstance(koptions, Options):
            koptions = Options(value=koptions)
            koptions.update(self._koptions)

        try:
            v_enc, flags = self._conn._tc.encode_value(koptions['value'],
                                                       koptions['format'])
        except Exception as ex:
            raise ValueFormatError.pyexc(str(ex))

        s_val = ffi.new('char[]', v_enc)
        self._cdata.append(s_val)

        req.bytes = s_val
        req.nbytes = len(v_enc)
        req.cas = koptions.get('cas', 0)
        req.exptime = koptions.get('ttl', 0)
        req.flags = flags
        req.operation = self._mode

class GetCommandContext(CommandContext):
    def __init__(self, parent, kv, ttl=0, is_lock=0, **kwargs):
        super(GetCommandContext, self).__init__(parent, 'lcb_get_cmd_t',
                                                **kwargs)
        self._koptions = Options({
            'ttl': ttl
        })
        self._is_lock = is_lock
        self.build(kv)

    def process_single_command(self, req, koptions):
        options = koptions.copy()
        options.update(self._koptions)

        req.exptime = options.get('ttl', 0)
        if self._is_lock:
            req.lock = 1

class RemoveCommandContext(CommandContext):
    def __init__(self, parent, kv, cas=0, **kwargs):
        super(RemoveCommandContext, self).__init__(parent,
                                                   'lcb_remove_cmd_t',
                                                   **kwargs)
        self._koptions = {
            'cas': cas
        }

        self.build(kv)

    def process_single_command(self, req, koptions):
        options = koptions.copy()
        options.update(self._koptions)
        req.cas = options.get('cas', 0)

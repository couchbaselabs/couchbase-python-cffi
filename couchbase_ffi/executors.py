import types

from couchbase._pyport import long, basestring, xrange
from couchbase.exceptions import ValueFormatError, ArgumentError, CouchbaseError
from couchbase.items import ItemCollection

from couchbase_ffi.result import (OperationResult, ValueResult, _SDResult, Item)
from couchbase_ffi.constants import FMT_UTF8, FMT_JSON
from couchbase_ffi.c import get_handle
from couchbase_ffi._rtconfig import pycbc_exc_lcb, pycbc_exc_enc, pycbc_exc_args, PyCBC
from couchbase_ffi.bufmanager import BufManager

ffi, C = get_handle()


class Options(dict):
    pass


def handle_durability(parent, **kwargs):
    """
    Handle durability requirements passed inside options
    :param parent: The parent bucket import
    :param kwargs: The arguments
    :return: A tuple of `(found, persist_to, replicate_to)`. The first
    element is True if either persistence or replication has been
    found
    """
    persist_to = kwargs.get('persist_to')
    replicate_to = kwargs.get('replicate_to')

    if not persist_to and not replicate_to:
        persist_to = parent._dur_persist_to
        replicate_to = parent._dur_replicate_to

    if not persist_to and not replicate_to:
        return False, 0, 0

    n_replicas = C.lcb_get_num_replicas(parent._lcbh)
    if replicate_to > n_replicas or persist_to > n_replicas+1:
        raise pycbc_exc_args('Durability requirements will never be satisfied')

    return True, persist_to, replicate_to


def create_key(tc, pykey):
    """
    Creates a C key from a Python key
    :param tc: The transcoder to use
    :param pykey: The python key to encode
    :return: A tuple of `encoded_key, encoded_length`
    """
    try:
        k_enc = tc.encode_key(pykey)
        if not k_enc:
            if not pykey:
                excls = ArgumentError
            else:
                excls = ValueFormatError
            raise excls.pyexc("Key is empty", obj=pykey)

    except (ValueFormatError, ArgumentError):
        raise
    except Exception as e:
        raise ValueFormatError.pyexc(inner=e)

    s_key = ffi.new('char[]', k_enc)
    return s_key, len(k_enc)


def get_option(name, key_options, global_options, default=None):
    """
    Search the key-specific options and the global options for a given
    setting. Either dictionary may be None.

    This will first search the key settings and then the global settings.

    :param name: The setting to search for
    :param key_options: The item specific settings
    :param global_options: General method parameters
    :return: The option, if found, or None
    """
    if key_options:
        try:
            return key_options[name]
        except KeyError:
            pass
    if global_options:
        try:
            return global_options[name]
        except KeyError:
            pass

    return default


def set_quiet(mres, parent, global_options):
    """
    Sets the 'quiet' property on the MultiResult
    """
    quiet = global_options.get('quiet')
    if quiet is not None:
        mres._quiet = quiet
    else:
        mres._quiet = parent.quiet


def get_cas(key_options, global_options, item):
    """
    Get the CAS from various inputs. This will properly honor
    the ``ignore_cas`` flag, if present.

    :param key_options: Key specific options
    :param global_options: Global options
    :param item: The item
    :return: The cas, or 0 if no cas
    """
    if item:
        ign_cas = get_option('ignore_cas', key_options, globals(), False)
        return 0 if ign_cas else item.cas
    else:
        try:
            cas = key_options['cas']
        except KeyError:
            try:
                cas = global_options['cas']
            except KeyError:
                return 0
        if not cas:
            return 0
        return cas


def process_opres_input(key, value, key_options):
    """
    Check if `value` or `key` is a Result object and populate the
    options accordingly.
    :param key:
    :param value:
    :param key_options:
    :return:
    """
    opres = None

    if isinstance(value, OperationResult):
        opres = value
    elif isinstance(key, OperationResult):
        opres = key
    elif isinstance(value, (long, int)):
        key_options['cas'] = value

    if opres is not None:
        key = opres.key
        key_options['cas'] = opres.cas
    return key, value, key_options


def get_ttl(key_options, global_options, *_):
    """
    Quick function to extract the expiration time from options. Throws
    appropriate exceptions when necessary
    :param key_options:
    :param global_options:
    :return:
    """
    ttl = get_option('ttl', key_options, global_options)
    if ttl is None or ttl == 0:
        return 0

    try:
        ttl = int(ttl)
        if ttl < 0:
            raise ArgumentError.pyexc("TTL cannot be negative", obj=ttl)
        elif ttl > 1 << 31:
            raise ArgumentError.pyexc("TTL Value too large", obj=ttl)
        return ttl
    except CouchbaseError:
        raise
    except Exception as e:
        raise ArgumentError.pyexc(inner=e, obj=ttl)


class BaseExecutor(object):
    """
    An executor class is intended to cache a single request object which may be
    used to schedule commands. Executors are stateless
    """

    STRUCTNAME = None
    """
    The name of the structure to allocate for a given command
    """

    FORBIDDEN_ITER = (basestring, bytearray, int,
                      long, float, type(None), bool)
    """
    Types forbidden from being used as iterators
    """

    VALUES_ALLOWED = False
    """
    Override in subclasses. This determines if simple (non-Item)
    values are allowed in the iterator, if the iterator is a dict
    """

    DUPKEY_OK = False
    """
    Whether duplicate keys are OK. This is typically false for everything
    but chained durability operations.
    """

    def __init__(self, conn):
        """
        Create a new executor
        :param conn: The parent connection
        """
        self.parent = conn
        self.c_command = ffi.new(self.STRUCTNAME+'*')

    @property
    def instance(self):
        return self.parent._lcbh

    def make_result(self, key, value):
        """
        Makes a single result which is then stored in the multi result object
        :param key: The actual key for the command
        :param value: The value passed (may be None)
        :return: A result object
        """
        v = OperationResult()
        v.key = key
        return v

    def make_entry_params(self, key, value, key_options):
        """
        Hook for subclasses to extract the actual Python key value and options
        for a given entry inside the iterator.
        :param key: The input key
        :param value: The input value
        :param key_options: The input options
        :return: A tuple of ``(key,value,options)``
        """
        return key, value, key_options

    def set_mres_flags(self, mres, kwargs):
        """
        Hook for subclasses to set flags on the result object
        :param mres: The MultiResult
        :param kwargs: Arguments passed to the command
        """
        pass

    @classmethod
    def _verify_iter(cls, kv):
        if isinstance(kv, (dict, list, tuple)):
            return

        if isinstance(kv, cls.FORBIDDEN_ITER):
            raise ArgumentError.pyexc(obj=kv, message="Bad sequence type")

        if not hasattr(kv, '__iter__'):
            raise ArgumentError.pyexc(obj=kv, message="Object is not iterable")

        try:
            len(kv)
        except TypeError:
            raise ArgumentError.pyexc(obj=kv,
                                      message="Iterator must have length")

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        """
        Submit a single item
        :param c_key: The pointer to the key
        :param c_len: The length of the key
        :param value: The value object. May be None
        :param item: The Item. May be None
        :param key_options: Key-specific options (may be None)
        :param global_options: Global options for the command
        :param mres: The MultiResult item. Used to create a cookie
        :return: A status code
        """
        raise NotImplementedError()

    def _invoke_submit(self, iterobj, is_dict, is_itmcoll, mres, global_kw):
        """
        Internal function to invoke the actual submit_single function
        :param iterobj: The raw object returned as the next item of the iterator
        :param is_dict: True if iterator is a dictionary
        :param is_itmcoll: True if the iterator contains Item objects
        :param mres: The multi result object
        :param global_kw: The global settings
        :return: The return value of :meth:`submit_single`
        """
        if is_itmcoll:
            item, key_options = next(iterobj)
            if not isinstance(item, Item):
                pycbc_exc_args('Expected item object')
            key = item.key
            value = item.value
            result = item
        else:
            if is_dict:
                key, value = next(iterobj)
                if not self.VALUES_ALLOWED and not is_itmcoll:
                    raise ArgumentError.pyexc(
                        'Values not allowed for this command', obj=value)
            else:
                key = next(iterobj)
                value = None

            key_options = {}
            item = None
            result = self.make_result(key, value)

        result.rc = -1

        # Attempt to get the encoded key:
        key, value, key_options = self.make_entry_params(key, value, key_options)
        c_key, c_len = create_key(self.parent._tc, key)

        rc = self.submit_single(c_key, c_len, value, item, key_options, global_kw, mres)
        if rc:
            raise pycbc_exc_lcb(rc)
        try:
            if key in mres and not self.DUPKEY_OK:
                # For tests:
                self.parent._warn_dupkey(key)

            mres[key] = result
        except TypeError:
            raise pycbc_exc_enc(obj=key)

    def execute(self, kv, **kwargs):
        """
        Execute the operation scheduling items as needed
        :param kv: An iterable of keys (or key-values, or Items)
        :param kwargs: Settings for the operation
        :return: A MultiResult object
        """
        self._verify_iter(kv)
        if not len(kv):
            raise ArgumentError.pyexc(obj=kv, message="No items in container")

        if isinstance(kv, dict):
            is_dict = True
            try:
                kviter = kv.iteritems()
            except AttributeError:
                kviter = iter(kv.items())
        else:
            is_dict = False
            kviter = iter(kv)

        is_itmcoll = isinstance(kv, ItemCollection)

        mres = kwargs.get('_MRES')
        if mres is None:
            mres = self.parent._make_mres()

        self.set_mres_flags(mres, kwargs)

        C.lcb_sched_enter(self.instance)
        num_items = 0
        while True:
            # Clear the previous command object
            C.memset(self.c_command, 0, ffi.sizeof(self.c_command[0]))

            try:
                self._invoke_submit(kviter, is_dict, is_itmcoll, mres, kwargs)
                num_items += 1
            except StopIteration:
                break
            except:
                C.lcb_sched_fail(self.instance)
                raise

        C.lcb_sched_leave(self.instance)
        mres._remaining += num_items
        # print "Execute(): mres:", mres
        return mres


class MultiContextExecutor(BaseExecutor):
    """
    Class which handles the proper allocation and destruction of the
    lcb_MULTICMD_CTX context
    """

    def create_context(self, **kwargs):
        """
        Implement in subclasses to return the actual multicmd pointer
        :return: A low level multi cmd context
        """
        raise NotImplementedError()

    def execute(self, kv, **kwargs):
        mctx = self.create_context(**kwargs)
        kwargs['_MCTX'] = mctx
        try:
            rv = super(MultiContextExecutor, self).execute(kv, **kwargs)
            C.lcb_sched_enter(self.instance)
            rc = mctx.done(mctx, rv._cdata)
            if rc:
                raise pycbc_exc_lcb(rc)

            C.lcb_sched_leave(self.instance)
            mctx = None
            return rv

        finally:
            if mctx is not None:
                mctx.fail(mctx)
                C.lcb_sched_fail(self.instance)


class StorageExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDSTORE'
    OPTYPE = None
    VALUES_ALLOWED = True

    def execute(self, kv, **kwargs):
        value_format = kwargs.get('format')
        if value_format is None:
            if self.OPTYPE not in (C.LCB_APPEND, C.LCB_PREPEND):
                value_format = self.parent.default_format
            else:
                value_format = FMT_UTF8
            # print "Setting format to", value_format
            kwargs['format'] = value_format

        return super(StorageExecutor, self).execute(kv, **kwargs)

    def set_mres_flags(self, mres, kwargs):
        ok, persist, replicate = handle_durability(self.parent, **kwargs)
        if ok:
            mres._dur = (persist, replicate)
        super(StorageExecutor, self).set_mres_flags(mres, kwargs)

    def submit_single(
            self, c_key, c_len, value, item, key_options, global_options, mres):

        value_format = get_option('format', key_options, global_options)
        if item:
            if self.OPTYPE in (C.LCB_APPEND, C.LCB_PREPEND):
                try:
                    value = key_options['fragment']
                except (KeyError, TypeError):
                    pycbc_exc_args('append/prepend must provide `fragment`')


        try:
            v_enc, flags = self.parent._tc.encode_value(value, value_format)
            if not isinstance(v_enc, bytes):
                raise ValueFormatError.pyexc("Value was not bytes", obj=v_enc)
            s_val = ffi.new('char[]', v_enc)
        except CouchbaseError:
            raise
        except Exception as ex:
            raise ValueFormatError.pyexc(str(value_format), inner=ex)

        C._Cb_set_key(self.c_command, c_key, c_len)
        C._Cb_set_val(self.c_command, s_val, len(v_enc))
        if self.OPTYPE not in (C.LCB_APPEND, C.LCB_PREPEND):
            try:
                self.c_command.flags = flags
            except OverflowError:
                pycbc_exc_enc('Invalid flags value', obj=flags)

        self.c_command.exptime = get_ttl(key_options, global_options, item)
        self.c_command.cas = get_cas(key_options, global_options, item)
        self.c_command.operation = self.OPTYPE
        return C.lcb_store3(self.instance, mres._cdata, self.c_command)


class AppendExecutor(StorageExecutor):
    OPTYPE = C.LCB_APPEND


class PrependExecutor(StorageExecutor):
    OPTYPE = C.LCB_PREPEND


class UpsertExecutor(StorageExecutor):
    OPTYPE = C.LCB_SET


class ReplaceExecutor(StorageExecutor):
    OPTYPE = C.LCB_REPLACE


class InsertExecutor(StorageExecutor):
    OPTYPE = C.LCB_ADD


class GetExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDGET'
    IS_LOCK = False
    IS_RGET = False

    def make_result(self, key, _):
        vr = ValueResult()
        vr.key = key
        return vr

    def set_mres_flags(self, mres, kwargs):
        set_quiet(mres, self.parent, kwargs)
        if kwargs.get('no_format'):
            mres._no_format = True
        super(GetExecutor, self).set_mres_flags(mres, kwargs)

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        ttl = get_ttl(key_options, global_options, item)
        if self.IS_LOCK and not ttl:
            raise ArgumentError.pyexc("Lock must have TTL")

        C._Cb_set_key(self.c_command, c_key, c_len)
        self.c_command.exptime = ttl
        self.c_command.lock = self.IS_LOCK
        return C.lcb_get3(self.instance, mres._cdata, self.c_command)

    def execute(self, kv, **kwargs):
        if kwargs.get('replica') and not isinstance(self, GetReplicaExecutor):
            del kwargs['replica']
            proc = self.parent._executors['_rget']
            return proc.execute(kv, **kwargs)

        return super(GetExecutor, self).execute(kv, **kwargs)


class GetReplicaExecutor(GetExecutor):
    STRUCTNAME = 'lcb_CMDGETREPLICA'

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        ix = get_option('replica', key_options, global_options, None)
        if ix is not None:
            self.c_command.index = ix
            self.c_command.strategy = C.LCB_REPLICA_SELECT
        else:
            self.c_command.strategy = C.LCB_REPLICA_FIRST

        C._Cb_set_key(self.c_command, c_key, c_len)
        return C.lcb_rget3(self.instance, mres._cdata, self.c_command)




class LockExecutor(GetExecutor):
    IS_LOCK = True


class RemoveExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDREMOVE'
    VALUES_ALLOWED = True

    def set_mres_flags(self, mres, kwargs):
        set_quiet(mres, self.parent, kwargs)
        ok, persist, replicate = handle_durability(self.parent, **kwargs)
        if ok:
            mres._dur = (persist, replicate)
        super(RemoveExecutor, self).set_mres_flags(mres, kwargs)

    def make_entry_params(self, key, value, key_options):
        return process_opres_input(key, value, key_options)

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        cas = get_cas(key_options, global_options, item)
        self.c_command.cas = cas
        C._Cb_set_key(self.c_command, c_key, c_len)
        return C.lcb_remove3(self.instance, mres._cdata, self.c_command)


class CounterExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDCOUNTER'

    def make_result(self, key, _):
        vr = ValueResult()
        vr.key = key
        return vr

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):

        delta = get_option('delta', key_options, global_options, 1)
        initial = get_option('initial', key_options, global_options)
        ttl = get_ttl(key_options, global_options)

        C._Cb_set_key(self.c_command, c_key, c_len)
        self.c_command.exptime = ttl
        self.c_command.delta = delta
        if initial is not None:
            self.c_command.initial = initial
            self.c_command.create = 1

        return C.lcb_counter3(self.instance, mres._cdata, self.c_command)


class SubdocExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDSUBDOC'
    VALUES_ALLOWED = True

    def make_result(self, key, value):
        vr = PyCBC.sd_result_type()  # type: _SDResult
        vr.key = key
        vr._specs = value
        return vr

    def __init__(self, *args):
        super(SubdocExecutor, self).__init__(*args)

    def _process_value(self, op, pyvalue, cspec, bm):
        MULTIVAL_OPS = (
            C.LCB_SDCMD_ARRAY_ADD_FIRST,
            C.LCB_SDCMD_ARRAY_ADD_LAST, C.LCB_SDCMD_ARRAY_INSERT)
        if isinstance(pyvalue, PyCBC.sd_multival_type) and op in MULTIVAL_OPS:
            is_multival = True
        else:
            is_multival = False

        encoded, _ = self.parent._tc.encode_value(pyvalue, FMT_JSON)
        if is_multival:
            encoded = encoded.strip()[1:-1]

        if not len(encoded):
            raise ValueFormatError.pyexc('Empty value passed', obj=pyvalue)

        c_value, c_len = bm.new_cbuf(encoded)
        # print(cspec, c_value, c_len)
        C._Cb_set_sdval(cspec, c_value, c_len)

    def _process_spec(self, pyspec, cspec, bm):
        """
        Process a single subdocument spec
        :param pyspec: Python spec (tuple)
        :param cspec: (out) - C spec
        :param BufManager bm:
        """
        op, path = pyspec[0], pyspec[1]
        c_path, c_pathlen = bm.new_cbuf(path)

        if len(pyspec) > 2:
            self._process_value(op, pyspec[2], cspec, bm)
            if len(pyspec) > 3:
                mkdir_p = pyspec[3]
                if mkdir_p:
                    cspec.options = C.LCB_SDSPEC_F_MKINTERMEDIATES

        C._Cb_set_sdpath(cspec, c_path, c_pathlen)
        cspec.sdcmd = op

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        if item:
            raise ArgumentError.pyexc('Item not allowed for subdoc')

        # Allocate the subdoc array
        if not isinstance(value, tuple):
            raise ArgumentError.pyexc('Value must be a tuple!')
        if not len(value):
            raise ArgumentError.pyexc('Need one or more commands')

        speclist = ffi.new('lcb_SDSPEC[{0}]'.format(len(value)))

        self.c_command.specs = speclist
        self.c_command.nspecs = len(value)
        self.c_command.cas = get_cas(key_options, global_options, item)
        C._Cb_set_key(self.c_command, c_key, c_len)

        bm = BufManager(ffi)

        for i in xrange(len(speclist)):
            pyspec = value[i]
            cspec = speclist + i
            self._process_spec(pyspec, cspec, bm)
        return C.lcb_subdoc3(self.instance, mres._cdata, self.c_command)


class SubdocLookupExecutor(SubdocExecutor):
    def set_mres_flags(self, mres, kwargs):
        set_quiet(mres, self.parent, kwargs)
        super(SubdocLookupExecutor, self).set_mres_flags(mres, kwargs)


class SubdocMutationExecutor(SubdocExecutor):
    def set_mres_flags(self, mres, kwargs):
        ok, persist, replicate = handle_durability(self.parent, **kwargs)
        if ok:
            mres._dur = (persist, replicate)
        super(SubdocMutationExecutor, self).set_mres_flags(mres, kwargs)


class UnlockExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDUNLOCK'
    VALUES_ALLOWED = True

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        cas = get_cas(key_options, global_options, item)
        if not cas:
            raise ArgumentError.pyexc("Must have CAS")

        C._Cb_set_key(self.c_command, c_key, c_len)
        self.c_command.cas = cas
        return C.lcb_unlock3(self.instance, mres._cdata, self.c_command)

    def make_entry_params(self, key, value, key_options):
        return process_opres_input(key, value, key_options)


class TouchExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDTOUCH'
    VALUES_ALLOWED = True

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        ttl = get_ttl(key_options, global_options)

        if not item and value is not None:
            if isinstance(value, dict):
                ttl = get_ttl(value, None)
            else:
                ttl = get_ttl({'ttl': value}, None)

        self.c_command.exptime = ttl
        C._Cb_set_key(self.c_command, c_key, c_len)
        return C.lcb_touch3(self.instance, mres._cdata, self.c_command)


class DurabilityExecutor(MultiContextExecutor):
    STRUCTNAME = 'lcb_CMDENDURE'
    VALUES_ALLOWED = True

    @staticmethod
    def _mk_criteria(opt, val):
        if val < 0:
            val = 255
            opt.cap_max = 1
        return val

    def __init__(self, *args):
        super(DurabilityExecutor, self).__init__(*args)
        self.c_options = ffi.new('lcb_durability_opts_t*')
        self.__opt = self.c_options.v.v0
        self.__errp = ffi.new('lcb_error_t*')

    def create_context(self, **kwargs):
        C.memset(self.c_options, 0, ffi.sizeof(self.c_options[0]))
        ok, persist_to, replicate_to = handle_durability(self.parent, **kwargs)
        if not ok:
            persist_to = -1
            replicate_to = -1

        self.__opt.persist_to = self._mk_criteria(self.__opt, persist_to)
        self.__opt.replicate_to = self._mk_criteria(self.__opt, replicate_to)

        if kwargs.get('check_removed'):
            self.__opt.check_delete = 1

        tmo = kwargs.get('timeout')
        if tmo:
            # print "Found timeout in options!"
            try:
                tmo = int(tmo * 1000000)
            except:
                raise pycbc_exc_args('Invalid timeout', obj=tmo)
        else:
            tmo = self.parent._dur_timeout

        if tmo:
            self.__opt.timeout = tmo

        # print "OPTIONS: "
        # print "PersistTo:", self.__opt.persist_to
        # print "ReplicateTo:", self.__opt.replicate_to
        # print "CapMax:", self.__opt.cap_max
        # print "Timeout:", self.__opt.timeout

        ctx = C.lcb_endure3_ctxnew(self.instance, self.c_options, self.__errp)
        if not ctx:
            raise pycbc_exc_lcb(self.__errp[0])
        return ctx

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        ctx = global_options['_MCTX']
        cas = get_cas(key_options, global_options, item)

        if not cas:
            if isinstance(value, OperationResult):
                cas = value.cas
            elif not isinstance(value, (int, long)):
                raise pycbc_exc_args('Bad CAS value', obj=cas)

        self.c_command.cas = cas
        C._Cb_set_key(self.c_command, c_key, c_len)

        # Add to the current context
        return ctx.addcmd(ctx, ffi.cast('lcb_CMDBASE*', self.c_command))


class DurabilityChainExecutor(DurabilityExecutor):
    """
    Subclass of DurabilityCommand executor which re-uses its result
    """

    # Because we have the item in from the previous result
    DUPKEY_OK = True

    def make_result(self, key, value):
        assert isinstance(value, OperationResult)
        return value


class ObserveExecutor(MultiContextExecutor):
    STRUCTNAME = 'lcb_CMDOBSERVE'

    def make_result(self, key, value):
        vr = ValueResult()
        vr.key = key
        vr.value = []
        return vr

    def create_context(self, **kwargs):
        return C.lcb_observe3_ctxnew(self.instance)

    def submit_single(self, c_key, c_len, value, item, key_options, global_options, mres):
        ctx = global_options['_MCTX']
        C._Cb_set_key(self.c_command, c_key, c_len)

        if get_option('master_only', key_options, global_options):
            self.c_command.cmdflags |= C.LCB_CMDOBSERVE_F_MASTER_ONLY
        return ctx.addcmd(ctx, ffi.cast('lcb_CMDBASE*', self.c_command))


class StatsExecutor(BaseExecutor):
    STRUCTNAME = 'lcb_CMDSTATS'

    def __run_stat(self, k, mres):
        bm = BufManager(ffi)
        if k:
            if not isinstance(k, basestring):
                raise pycbc_exc_args('Stats arguments must be strings only!')
            c_key, c_len = bm.new_cbuf(k)
        else:
            c_key, c_len = ffi.NULL, 0

        C._Cb_set_key(self.c_command, c_key, c_len)
        rc = C.lcb_stats3(self.instance, mres._cdata, self.c_command)
        if rc:
            raise pycbc_exc_lcb(rc)

    def execute(self, kv, **kwargs):
        C.lcb_sched_enter(self.instance)
        mres = self.parent._make_mres()

        if not kv or not len(kv):
            kv = ['']

        self.c_command.cmdflags = \
            C.LCB_CMDSTATS_F_KV if kwargs.get('keystats') else 0

        for key in kv:
            C.memset(self.c_command, 0, ffi.sizeof(self.c_command[0]))
            try:
                self.__run_stat(key, mres)
                mres._remaining += 1
            except:
                C.lcb_sched_fail(self.instance)
                raise

        C.lcb_sched_leave(self.instance)
        return mres
from couchbase_ffi._cinit import get_handle
from couchbase_ffi.constants import (
    PYCBC_EVACTION_WATCH, PYCBC_EVACTION_UNWATCH,
    PYCBC_EVACTION_CLEANUP, PYCBC_EVSTATE_ACTIVE,
    PYCBC_EVSTATE_SUSPENDED,
    LCB_READ_EVENT, LCB_WRITE_EVENT)


ffi, C = get_handle()


class Event(object):
    __slots__ = ['evtype', 'state', '_c_callback', '_c_arg', '_cdata']

    def __init__(self):
        self._cdata = ffi.new_handle(self)
        self.state = 0


class IOEvent(Event):
    __slots__ = ['fd', 'flags']

    def ready_r(self):
        C._Cb_do_callback(self.fd, LCB_READ_EVENT, self._c_callback, self._c_arg)

    def ready_w(self):
        C._Cb_do_callback(self.fd, LCB_WRITE_EVENT, self._c_callback, self._c_arg)

    def ready(self, flags):
        C._Cb_do_callback(self.fd, flags, self._c_callback, self._c_arg)

    def fileno(self):
        return self.fd


class TimerEvent(Event):
    def ready(self, *args):
        C._Cb_do_callback(0, 0, self._c_callback, self._c_arg)


def to_pyio(fn):
    def wrap(*args):
        iobj = args[0]
        obj = ffi.from_handle(iobj.v.v0.cookie)
        return fn(obj, *args)
    return wrap

@ffi.callback('void*(lcb_io_opt_t)')
@to_pyio
def create_timer(self, io):
    return self.new_event_common(self._do_create_timer)

@ffi.callback('void*(lcb_io_opt_t)')
@to_pyio
def create_event(self, io):
    return self.new_event_common(self._do_create_event)

@ffi.callback('void(lcb_io_opt_t,void*)')
@to_pyio
def destroy_common(self, io, arg):
    event = ffi.from_handle(arg)
    self.free_event_common(event)

@ffi.callback('int(lcb_io_opt_t,void*,lcb_U32,void*,lcb_ioE_callback)')
@to_pyio
def update_timer(self, io, cdata_timer, usec, arg, callback):
    timer = ffi.from_handle(cdata_timer)
    timer._c_callback = callback
    timer._c_arg = arg
    self.mod_event_common(timer, PYCBC_EVACTION_WATCH, 0, usec)
    return 0

@ffi.callback('void(lcb_io_opt_t,void*)')
@to_pyio
def delete_timer(self, io, cdata_timer):
    timer = ffi.from_handle(cdata_timer)
    self.mod_event_common(timer, PYCBC_EVACTION_UNWATCH, 0, 0)

@ffi.callback('int(lcb_io_opt_t,lcb_socket_t,void*,short,void*,lcb_ioE_callback)')
@to_pyio
def update_event(self, io, sock, event_cdata, flags, arg, callback):
    event = ffi.from_handle(event_cdata)
    event._c_callback = callback
    event._c_arg = arg
    self.mod_event_common(event, PYCBC_EVACTION_WATCH, sock, flags)
    return 0

@ffi.callback('void(lcb_io_opt_t,lcb_socket_t,void*)')
@to_pyio
def delete_event(self, io, sock, event_cdata):
    event = ffi.from_handle(event_cdata)
    self.mod_event_common(event, PYCBC_EVACTION_UNWATCH, sock, 0)

@ffi.callback('void(lcb_io_opt_t)')
@to_pyio
def run_loop(self, io):
    self._do_start()

@ffi.callback('void(lcb_io_opt_t)')
@to_pyio
def stop_loop(self, io):
    self._do_stop()


@ffi.callback('''void(
    int,
    lcb_loop_procs*,
    lcb_timer_procs*,
    lcb_bsd_procs*,
    lcb_ev_procs*,
    lcb_completion_procs*,
    lcb_iomodel_t*)''')
def getprocs(version,
             loop_procs,
             timer_procs,
             bsd_procs,
             ev_procs,
             completion_procs,
             iomodel):
    C.lcb_iops_wire_bsd_impl2(bsd_procs, version)

    timer_procs.create = create_timer
    timer_procs.destroy = destroy_common
    timer_procs.schedule = update_timer
    timer_procs.cancel = delete_timer
    ev_procs.create = create_event
    ev_procs.destroy = destroy_common
    ev_procs.watch = update_event
    ev_procs.cancel = delete_event
    loop_procs.start = run_loop
    loop_procs.stop = stop_loop

    iomodel[0] = C.LCB_IOMODEL_EVENT


class IOPSWrapper(object):
    def __init__(self, procs_obj):
        self._pyprocs = procs_obj

        # Get all the I/O methods from the inner object
        self._do_update_event = procs_obj.update_event
        self._do_update_timer = procs_obj.update_timer
        self._do_create_timer = getattr(procs_obj, 'timer_event_factory',
                                        self._default_timer_factory)
        self._do_create_event = getattr(procs_obj, 'io_event_factory',
                                        self._default_event_factory())
        self._do_start = getattr(procs_obj, 'start_watching',
                                 self._default_start())
        self._do_stop = getattr(procs_obj, 'stop_watching',
                                self._default_stop())

        self._cdata = ffi.new_handle(self)

        self._c_iops = ffi.new('lcb_io_opt_t')
        self._c_iops.version = 2
        self._c_iops.v.v2.cookie = self._cdata
        self._c_iops.v.v2.get_procs = getprocs
        self._handles = {}

    def get_lcb_iops(self):
        return self._c_iops

    def _default_timer_factory(self):
        return TimerEvent()

    def _default_event_factory(self):
        return IOEvent

    def _default_start(self):
        pass

    def _default_stop(self):
        pass

    def mod_event_common(self, event, action, newsock, extra):
        if isinstance(event, IOEvent):
            # Extra is flags
            if newsock is not None:
                event.fd = newsock
            self._do_update_event(event, action, extra)
            event.flags = extra
        else:
            self._do_update_timer(event, action, extra)

        if action == PYCBC_EVACTION_WATCH:
            event.state = PYCBC_EVSTATE_ACTIVE
        else:
            event.state = PYCBC_EVSTATE_SUSPENDED

    def new_event_common(self, fn):
        event = fn()
        self._handles[id(event)] = event
        return event._cdata

    def free_event_common(self, ev):
        self.mod_event_common(ev, PYCBC_EVACTION_CLEANUP, None, 0)
        del ev._cdata
        del self._handles[id(ev)]
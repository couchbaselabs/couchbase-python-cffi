typedef unsigned long size_t;
typedef int __builtin_va_list;
typedef int __gnuc_va_list;
typedef int __int8_t;
typedef int __uint8_t;
typedef int __int16_t;
typedef int __uint16_t;
typedef int __int_least16_t;
typedef int __uint_least16_t;
typedef int __int32_t;
typedef int __uint32_t;
typedef int __int64_t;
typedef int __uint64_t;
typedef int __int_least32_t;
typedef int __uint_least32_t;
typedef int _LOCK_T;
typedef int _LOCK_RECURSIVE_T;
typedef int _off_t;
typedef int __dev_t;
typedef int __uid_t;
typedef int __gid_t;
typedef int _off64_t;
typedef int _fpos_t;
typedef int _ssize_t;
typedef int wint_t;
typedef int _mbstate_t;
typedef int _flock_t;
typedef int _iconv_t;
typedef int __ULong;
typedef int __FILE;
typedef int ptrdiff_t;
typedef int wchar_t;
typedef int __off_t;
typedef int __pid_t;
typedef int __loff_t;
typedef int u_char;
typedef int u_short;
typedef int u_int;
typedef int u_long;
typedef int ushort;
typedef int uint;
typedef int clock_t;
typedef unsigned long time_t;
typedef int daddr_t;
typedef int caddr_t;
typedef int ino_t;
typedef int off_t;
typedef int dev_t;
typedef int uid_t;
typedef int gid_t;
typedef int pid_t;
typedef int key_t;
typedef int ssize_t;
typedef int mode_t;
typedef int nlink_t;
typedef int fd_mask;
typedef int _types_fd_set;
typedef int clockid_t;
typedef int timer_t;
typedef int useconds_t;
typedef int suseconds_t;
typedef int FILE;
typedef int fpos_t;
typedef int cookie_read_function_t;
typedef int cookie_write_function_t;
typedef int cookie_seek_function_t;
typedef int cookie_close_function_t;
typedef int cookie_io_functions_t;
typedef int div_t;
typedef int ldiv_t;
typedef int lldiv_t;
typedef int sigset_t;
typedef int __sigset_t;
typedef int _sig_func_ptr;
typedef int sig_atomic_t;
typedef int __tzrule_type;
typedef int __tzinfo_type;
typedef int mbstate_t;
typedef int sem_t;
typedef int pthread_t;
typedef int pthread_attr_t;
typedef int pthread_mutex_t;
typedef int pthread_mutexattr_t;
typedef int pthread_cond_t;
typedef int pthread_condattr_t;
typedef int pthread_key_t;
typedef int pthread_once_t;
typedef int pthread_rwlock_t;
typedef int pthread_rwlockattr_t;
typedef int pthread_spinlock_t;
typedef int pthread_barrier_t;
typedef int pthread_barrierattr_t;
typedef int jmp_buf;
typedef int sigjmp_buf;
typedef int stack_t;
typedef char int8_t;
typedef unsigned char uint8_t;
typedef short int16_t;
typedef unsigned short uint16_t;
typedef int int32_t;
typedef unsigned uint32_t;
typedef long long int64_t;
typedef unsigned long long uint64_t;
typedef int int_least8_t;
typedef int uint_least8_t;
typedef int int_least16_t;
typedef int uint_least16_t;
typedef int int_least32_t;
typedef int uint_least32_t;
typedef int int_least64_t;
typedef int uint_least64_t;
typedef int int_fast8_t;
typedef int uint_fast8_t;
typedef int int_fast16_t;
typedef int uint_fast16_t;
typedef int int_fast32_t;
typedef int uint_fast32_t;
typedef int int_fast64_t;
typedef int uint_fast64_t;
typedef int intptr_t;
typedef int uintptr_t;
typedef int intmax_t;
typedef int uintmax_t;
typedef _Bool bool;
typedef int va_list;
    typedef int64_t lcb_int64_t;
    typedef int32_t lcb_int32_t;
    typedef size_t lcb_size_t;
    typedef ssize_t lcb_ssize_t;
    typedef uint16_t lcb_vbucket_t;
    typedef uint8_t lcb_uint8_t;
    typedef uint16_t lcb_uint16_t;
    typedef uint32_t lcb_uint32_t;
    typedef uint64_t lcb_cas_t;
    typedef uint64_t lcb_uint64_t;
    typedef time_t lcb_time_t;
typedef lcb_int64_t lcb_S64;
typedef lcb_uint64_t lcb_U64;
typedef lcb_uint32_t lcb_U32;
typedef lcb_int32_t lcb_S32;
typedef lcb_uint16_t lcb_U16;
typedef lcb_uint8_t lcb_U8;
typedef lcb_size_t lcb_SIZE;
typedef lcb_ssize_t lcb_SSIZE;
typedef lcb_time_t lcb_SECS;
typedef lcb_cas_t lcb_CAS;
struct lcb_st;
typedef struct lcb_st *lcb_t;
struct lcb_http_request_st;
typedef struct lcb_http_request_st *lcb_http_request_t;
typedef enum {
LCB_ERRTYPE_INPUT=1,
LCB_ERRTYPE_NETWORK=2,
LCB_ERRTYPE_FATAL=4,
LCB_ERRTYPE_TRANSIENT=8,
LCB_ERRTYPE_DATAOP=16,
LCB_ERRTYPE_INTERNAL=32,
LCB_ERRTYPE_PLUGIN=64,
LCB_ERRTYPE_SRVLOAD=128,
LCB_ERRTYPE_SRVGEN=256,
} lcb_errflags_t;
typedef enum {
LCB_SUCCESS=0,LCB_AUTH_CONTINUE=1,LCB_AUTH_ERROR=2,LCB_DELTA_BADVAL=3,LCB_E2BIG=4,LCB_EBUSY=5,LCB_EINTERNAL=6,LCB_EINVAL=7,LCB_ENOMEM=8,LCB_ERANGE=9,LCB_ERROR=10,LCB_ETMPFAIL=11,LCB_KEY_EEXISTS=12,LCB_KEY_ENOENT=13,LCB_DLOPEN_FAILED=14,LCB_DLSYM_FAILED=15,LCB_NETWORK_ERROR=16,LCB_NOT_MY_VBUCKET=17,LCB_NOT_STORED=18,LCB_NOT_SUPPORTED=19,LCB_UNKNOWN_COMMAND=20,LCB_UNKNOWN_HOST=21,LCB_PROTOCOL_ERROR=22,LCB_ETIMEDOUT=23,LCB_CONNECT_ERROR=24,LCB_BUCKET_ENOENT=25,LCB_CLIENT_ENOMEM=26,LCB_CLIENT_ETMPFAIL=27,LCB_EBADHANDLE=28,LCB_SERVER_BUG=29,LCB_PLUGIN_VERSION_MISMATCH=30,LCB_INVALID_HOST_FORMAT=31,LCB_INVALID_CHAR=32,LCB_DURABILITY_ETOOMANY=33,LCB_DUPLICATE_COMMANDS=34,LCB_NO_MATCHING_SERVER=35,LCB_BAD_ENVIRONMENT=36,LCB_BUSY=37,LCB_INVALID_USERNAME=38,LCB_CONFIG_CACHE_INVALID=39,LCB_SASLMECH_UNAVAILABLE=40,LCB_TOO_MANY_REDIRECTS=41,LCB_MAP_CHANGED=42,LCB_INCOMPLETE_PACKET=43,LCB_ECONNREFUSED=44,LCB_ESOCKSHUTDOWN=45,LCB_ECONNRESET=46,LCB_ECANTGETPORT=47,LCB_EFDLIMITREACHED=48,LCB_ENETUNREACH=49,LCB_ECTL_UNKNOWN=50,LCB_ECTL_UNSUPPMODE=51,LCB_ECTL_BADARG=52,LCB_EMPTY_KEY=53,LCB_SSL_ERROR=54,LCB_SSL_CANTVERIFY=55,
LCB_MAX_ERROR=4096,
} lcb_error_t;
int lcb_get_errtype(lcb_error_t err);
const char *lcb_strerror(lcb_t instance, lcb_error_t error);
typedef int lcb_socket_t;
struct sockaddr;
typedef struct lcb_iovec_st {
    void *iov_base;
    size_t iov_len;
} lcb_IOV;
struct lcb_nameinfo_st {
    struct {
        struct sockaddr *name;
        int *len;
    } local;
    struct {
        struct sockaddr *name;
        int *len;
    } remote;
};
typedef struct lcb_io_opt_st* lcb_io_opt_t;
typedef void (*lcb_ioE_callback)
        (lcb_socket_t sock, short events, void *uarg);
typedef void *(*lcb_io_timer_create_fn)
        (lcb_io_opt_t iops);
typedef void (*lcb_io_timer_destroy_fn)
        (lcb_io_opt_t iops, void *timer);
typedef void (*lcb_io_timer_cancel_fn)
        (lcb_io_opt_t iops, void *timer);
typedef int (*lcb_io_timer_schedule_fn)
        (lcb_io_opt_t iops, void *timer,
                lcb_U32 usecs,
                void *uarg,
                lcb_ioE_callback callback);
typedef void *(*lcb_ioE_event_create_fn)
        (lcb_io_opt_t iops);
typedef void (*lcb_ioE_event_destroy_fn)
        (lcb_io_opt_t iops, void *event);
typedef void (*lcb_ioE_event_cancel_fn)
        (lcb_io_opt_t iops, lcb_socket_t sock, void *event);
typedef int (*lcb_ioE_event_watch_fn)
        (lcb_io_opt_t iops,
                lcb_socket_t socket,
                void *event,
                short evflags,
                void *uarg,
                lcb_ioE_callback callback);
typedef lcb_SSIZE (*lcb_ioE_recv_fn)
        (lcb_io_opt_t iops, lcb_socket_t sock, void *target_buf,
                lcb_SIZE buflen, int _unused_flags);
typedef lcb_SSIZE (*lcb_ioE_send_fn)
        (lcb_io_opt_t iops, lcb_socket_t sock, const void *srcbuf,
                lcb_SIZE buflen, int _ignored);
typedef lcb_SSIZE (*lcb_ioE_recvv_fn)
        (lcb_io_opt_t iops, lcb_socket_t sock, lcb_IOV *iov, lcb_SIZE niov);
typedef lcb_SSIZE (*lcb_ioE_sendv_fn)
        (lcb_io_opt_t iops, lcb_socket_t sock, lcb_IOV *iov, lcb_SIZE niov);
typedef lcb_socket_t (*lcb_ioE_socket_fn)
        (lcb_io_opt_t iops, int domain, int type, int protocol);
typedef int (*lcb_ioE_connect_fn)
        (lcb_io_opt_t iops,
                lcb_socket_t sock,
                const struct sockaddr *dst,
                unsigned int addrlen);
typedef int (*lcb_ioE_bind_fn)
        (lcb_io_opt_t iops,
                lcb_socket_t sock,
                const struct sockaddr *srcaddr,
                unsigned int addrlen);
typedef int (*lcb_ioE_listen_fn)
        (lcb_io_opt_t iops,
                lcb_socket_t bound_sock,
                unsigned int queuelen);
typedef lcb_socket_t (*lcb_ioE_accept_fn)
        (lcb_io_opt_t iops,
                lcb_socket_t lsnsock);
typedef void (*lcb_ioE_close_fn)
        (lcb_io_opt_t iops, lcb_socket_t sock);
struct ringbuffer_st;
struct lcb_connection_st;
struct lcbio_SOCKET;
struct lcb_buf_info {
    char *root;
    lcb_SIZE size;
    struct ringbuffer_st *ringbuffer;
    struct lcb_iovec_st iov[2];
};
typedef struct lcb_sockdata_st {
    lcb_socket_t socket;
    lcb_io_opt_t parent;
    struct lcbio_SOCKET *lcbconn;
    int closed;
    int is_reading;
    struct lcb_buf_info read_buffer;
} lcb_sockdata_t;
typedef struct lcb_io_writebuf_st {
    struct lcb_io_opt_st *parent;
    struct lcb_buf_info buffer;
} lcb_io_writebuf_t;
typedef lcb_sockdata_t* (*lcb_ioC_socket_fn)
        (lcb_io_opt_t iops, int domain, int type, int protocol);
typedef void (*lcb_io_connect_cb)(lcb_sockdata_t *socket, int status);
typedef int (*lcb_ioC_connect_fn)
        (lcb_io_opt_t iops, lcb_sockdata_t *sd,
                const struct sockaddr *dst,
                unsigned int naddr,
                lcb_io_connect_cb callback);
typedef void (lcb_ioC_serve_callback)
        (lcb_sockdata_t *sd_server,
                lcb_sockdata_t *sd_client,
                int status);
typedef int (*lcb_ioC_serve_fn)
        (lcb_io_opt_t iops,
                lcb_sockdata_t *server_socket,
                const struct sockaddr *listen_addr,
                lcb_ioC_serve_callback callback);
typedef int (*lcb_ioC_nameinfo_fn)
        (lcb_io_opt_t iops,
                lcb_sockdata_t *sock,
                struct lcb_nameinfo_st *ni);
typedef void (*lcb_ioC_read_callback)(lcb_sockdata_t *sd, lcb_SSIZE nread);
typedef int (*lcb_ioC_read_fn)(lcb_io_opt_t,lcb_sockdata_t*,lcb_ioC_read_callback);
typedef lcb_io_writebuf_t* (*lcb_ioC_wballoc_fn)(lcb_io_opt_t,lcb_sockdata_t *);
typedef void (*lcb_ioC_wbfree_fn)(lcb_io_opt_t,lcb_sockdata_t*,lcb_io_writebuf_t*);
typedef void (*lcb_ioC_write_callback)(lcb_sockdata_t*,lcb_io_writebuf_t*,int);
typedef int (*lcb_ioC_write_fn)
        (lcb_io_opt_t,lcb_sockdata_t*,lcb_io_writebuf_t*,lcb_ioC_write_callback);
typedef void (*lcb_ioC_write2_callback)
        (lcb_sockdata_t *sd,
                int status,
                void *arg);
typedef int (*lcb_ioC_write2_fn)
        (lcb_io_opt_t iops,
                lcb_sockdata_t *sd,
                lcb_IOV *iov,
                lcb_SIZE niov,
                void *uarg,
                lcb_ioC_write2_callback callback);
typedef void (*lcb_ioC_read2_callback)
        (lcb_sockdata_t *sd, lcb_SSIZE nread, void *arg);
typedef int (*lcb_ioC_read2_fn)
        (lcb_io_opt_t iops,
                lcb_sockdata_t *sd,
                lcb_IOV *iov,
                lcb_SIZE niov,
                void *uarg,
                lcb_ioC_read2_callback callback);
typedef unsigned int (*lcb_ioC_close_fn)
        (lcb_io_opt_t iops,
                lcb_sockdata_t *sd);
typedef void (*lcb_io_start_fn)(lcb_io_opt_t iops);
typedef void (*lcb_io_stop_fn)(lcb_io_opt_t iops);
typedef void (*lcb_io_error_cb)(lcb_sockdata_t *socket) ;
struct lcb_iops_evented_st {
    void *cookie; int error; int need_cleanup;
    lcb_ioE_socket_fn socket;
    lcb_ioE_connect_fn connect;
    lcb_ioE_recv_fn recv;
    lcb_ioE_send_fn send;
    lcb_ioE_recvv_fn recvv;
    lcb_ioE_sendv_fn sendv;
    lcb_ioE_close_fn close;
    lcb_io_timer_create_fn create_timer;
    lcb_io_timer_destroy_fn destroy_timer;
    lcb_io_timer_cancel_fn delete_timer;
    lcb_io_timer_schedule_fn update_timer;
    lcb_ioE_event_create_fn create_event;
    lcb_ioE_event_destroy_fn destroy_event;
    lcb_ioE_event_watch_fn update_event;
    lcb_ioE_event_cancel_fn delete_event;
    lcb_io_stop_fn stop_event_loop;
    lcb_io_start_fn run_event_loop;
};
struct lcb_iops_completion_st {
    void *cookie; int error; int need_cleanup;
    lcb_ioC_socket_fn create_socket;
    lcb_ioC_connect_fn start_connect;
    lcb_ioC_wballoc_fn create_writebuf;
    lcb_ioC_wbfree_fn release_writebuf;
    lcb_ioC_write_fn start_write;
    lcb_ioC_read_fn start_read;
    lcb_ioC_close_fn close_socket;
    lcb_io_timer_create_fn create_timer;
    lcb_io_timer_destroy_fn destroy_timer;
    lcb_io_timer_cancel_fn delete_timer;
    lcb_io_timer_schedule_fn update_timer;
    lcb_ioC_nameinfo_fn get_nameinfo;
    void (*pad1)(void);
    void (*pad2)(void);
    void (*send_error)(struct lcb_io_opt_st*, lcb_sockdata_t*,void(*)(lcb_sockdata_t*));
    lcb_io_stop_fn stop_event_loop;
    lcb_io_start_fn run_event_loop;
};
typedef struct lcb_timerprocs_st {
    lcb_io_timer_create_fn create;
    lcb_io_timer_destroy_fn destroy;
    lcb_io_timer_cancel_fn cancel;
    lcb_io_timer_schedule_fn schedule;
} lcb_timer_procs;
typedef struct lcb_loopprocs_st {
    lcb_io_start_fn start;
    lcb_io_stop_fn stop;
} lcb_loop_procs;
typedef struct lcb_bsdprocs_st {
    lcb_ioE_socket_fn socket0;
    lcb_ioE_connect_fn connect0;
    lcb_ioE_recv_fn recv;
    lcb_ioE_recvv_fn recvv;
    lcb_ioE_send_fn send;
    lcb_ioE_sendv_fn sendv;
    lcb_ioE_close_fn close;
    lcb_ioE_bind_fn bind;
    lcb_ioE_listen_fn listen;
    lcb_ioE_accept_fn accept;
} lcb_bsd_procs;
typedef struct lcb_evprocs_st {
    lcb_ioE_event_create_fn create;
    lcb_ioE_event_destroy_fn destroy;
    lcb_ioE_event_cancel_fn cancel;
    lcb_ioE_event_watch_fn watch;
} lcb_ev_procs;
typedef struct {
    lcb_ioC_socket_fn socket;
    lcb_ioC_close_fn close;
    lcb_ioC_read_fn read;
    lcb_ioC_connect_fn connect;
    lcb_ioC_wballoc_fn wballoc;
    lcb_ioC_wbfree_fn wbfree;
    lcb_ioC_write_fn write;
    lcb_ioC_write2_fn write2;
    lcb_ioC_read2_fn read2;
    lcb_ioC_serve_fn serve;
    lcb_ioC_nameinfo_fn nameinfo;
} lcb_completion_procs;
typedef enum {
    LCB_IOMODEL_EVENT,
    LCB_IOMODEL_COMPLETION
} lcb_iomodel_t;
typedef void (*lcb_io_procs_fn)
        (int version,
                lcb_loop_procs *loop_procs,
                lcb_timer_procs *timer_procs,
                lcb_bsd_procs *bsd_procs,
                lcb_ev_procs *ev_procs,
                lcb_completion_procs *completion_procs,
                lcb_iomodel_t *iomodel);
struct lcbio_TABLE;
struct lcb_iops2_st {
    void *cookie; int error; int need_cleanup;
    lcb_io_procs_fn get_procs;
    struct lcbio_TABLE *iot;
};
struct lcb_io_opt_st {
    int version;
    void *dlhandle;
    void (*destructor)(struct lcb_io_opt_st *iops);
    union {
        struct {
            void *cookie; int error; int need_cleanup;
        } base;
        struct lcb_iops_evented_st v0;
        struct lcb_iops_completion_st v1;
        struct lcb_iops2_st v2;
    } v;
};
typedef lcb_error_t (*lcb_io_create_fn)
        (int version, lcb_io_opt_t *io, void *cookie);
    typedef enum {
LCB_HTTP_STATUS_CONTINUE=100,
LCB_HTTP_STATUS_SWITCHING_PROTOCOLS=101,
LCB_HTTP_STATUS_PROCESSING=102,
LCB_HTTP_STATUS_OK=200,
LCB_HTTP_STATUS_CREATED=201,
LCB_HTTP_STATUS_ACCEPTED=202,
LCB_HTTP_STATUS_NON_AUTHORITATIVE_INFORMATION=203,
LCB_HTTP_STATUS_NO_CONTENT=204,
LCB_HTTP_STATUS_RESET_CONTENT=205,
LCB_HTTP_STATUS_PARTIAL_CONTENT=206,
LCB_HTTP_STATUS_MULTI_STATUS=207,
LCB_HTTP_STATUS_MULTIPLE_CHOICES=300,
LCB_HTTP_STATUS_MOVED_PERMANENTLY=301,
LCB_HTTP_STATUS_FOUND=302,
LCB_HTTP_STATUS_SEE_OTHER=303,
LCB_HTTP_STATUS_NOT_MODIFIED=304,
LCB_HTTP_STATUS_USE_PROXY=305,
LCB_HTTP_STATUS_UNUSED=306,
LCB_HTTP_STATUS_TEMPORARY_REDIRECT=307,
LCB_HTTP_STATUS_BAD_REQUEST=400,
LCB_HTTP_STATUS_UNAUTHORIZED=401,
LCB_HTTP_STATUS_PAYMENT_REQUIRED=402,
LCB_HTTP_STATUS_FORBIDDEN=403,
LCB_HTTP_STATUS_NOT_FOUND=404,
LCB_HTTP_STATUS_METHOD_NOT_ALLOWED=405,
LCB_HTTP_STATUS_NOT_ACCEPTABLE=406,
LCB_HTTP_STATUS_PROXY_AUTHENTICATION_REQUIRED=407,
LCB_HTTP_STATUS_REQUEST_TIMEOUT=408,
LCB_HTTP_STATUS_CONFLICT=409,
LCB_HTTP_STATUS_GONE=410,
LCB_HTTP_STATUS_LENGTH_REQUIRED=411,
LCB_HTTP_STATUS_PRECONDITION_FAILED=412,
LCB_HTTP_STATUS_REQUEST_ENTITY_TOO_LARGE=413,
LCB_HTTP_STATUS_REQUEST_URI_TOO_LONG=414,
LCB_HTTP_STATUS_UNSUPPORTED_MEDIA_TYPE=415,
LCB_HTTP_STATUS_REQUESTED_RANGE_NOT_SATISFIABLE=416,
LCB_HTTP_STATUS_EXPECTATION_FAILED=417,
LCB_HTTP_STATUS_UNPROCESSABLE_ENTITY=422,
LCB_HTTP_STATUS_LOCKED=423,
LCB_HTTP_STATUS_FAILED_DEPENDENCY=424,
LCB_HTTP_STATUS_INTERNAL_SERVER_ERROR=500,
LCB_HTTP_STATUS_NOT_IMPLEMENTED=501,
LCB_HTTP_STATUS_BAD_GATEWAY=502,
LCB_HTTP_STATUS_SERVICE_UNAVAILABLE=503,
LCB_HTTP_STATUS_GATEWAY_TIMEOUT=504,
LCB_HTTP_STATUS_HTTP_VERSION_NOT_SUPPORTED=505,
LCB_HTTP_STATUS_INSUFFICIENT_STORAGE=507,
    } lcb_http_status_t;
typedef lcb_U8 lcb_datatype_t;
typedef lcb_U32 lcb_USECS;
typedef enum {
LCB_CONFIG_TRANSPORT_LIST_END=0,
LCB_CONFIG_TRANSPORT_HTTP=1,
    LCB_CONFIG_TRANSPORT_CCCP,
    LCB_CONFIG_TRANSPORT_MAX
} lcb_config_transport_t;
typedef enum {
LCB_TYPE_BUCKET=0,
LCB_TYPE_CLUSTER=1,
} lcb_type_t;
struct lcb_create_st0 { const char *host; const char *user; const char *passwd; const char *bucket; struct lcb_io_opt_st *io; };
struct lcb_create_st1 { const char *host; const char *user; const char *passwd; const char *bucket; struct lcb_io_opt_st *io; lcb_type_t type; };
struct lcb_create_st2 { const char *host; const char *user; const char *passwd; const char *bucket; struct lcb_io_opt_st *io; lcb_type_t type; const char *mchosts; const lcb_config_transport_t* transports; };
struct lcb_create_st3 {
    const char *connstr;
    const char *username;
    const char *passwd;
    void *_pad_bucket;
    struct lcb_io_opt_st *io;
    lcb_type_t type;
};
struct lcb_create_st {
    int version;
    union {
        struct lcb_create_st0 v0;
        struct lcb_create_st1 v1;
        struct lcb_create_st2 v2;
        struct lcb_create_st3 v3;
    } v;
};
lcb_error_t lcb_create(lcb_t *instance,
                       const struct lcb_create_st *options);
lcb_error_t lcb_connect(lcb_t instance);
void lcb_set_cookie(lcb_t instance, const void *cookie);
const void *lcb_get_cookie(lcb_t instance);
lcb_error_t lcb_wait(lcb_t instance);
typedef enum {
LCB_WAIT_DEFAULT=0,
LCB_WAIT_NOCHECK=1,
} lcb_WAITFLAGS;
void lcb_wait3(lcb_t instance, lcb_WAITFLAGS flags);
void lcb_breakout(lcb_t instance);
typedef void (*lcb_bootstrap_callback)(lcb_t instance, lcb_error_t err);
lcb_bootstrap_callback
lcb_set_bootstrap_callback(lcb_t instance, lcb_bootstrap_callback callback);
lcb_error_t
lcb_get_bootstrap_status(lcb_t instance);
void
lcb_refresh_config(lcb_t instance);
typedef enum {
LCB_CONFIGURATION_NEW=0,
LCB_CONFIGURATION_CHANGED=1,
LCB_CONFIGURATION_UNCHANGED=2,
} lcb_configuration_t;
typedef void (*lcb_configuration_callback)(lcb_t instance,
                                           lcb_configuration_t config);
lcb_configuration_callback
lcb_set_configuration_callback(lcb_t, lcb_configuration_callback);
void lcb_destroy(lcb_t instance);
typedef void (*lcb_destroy_callback)(const void *cookie);
lcb_destroy_callback
lcb_set_destroy_callback(lcb_t, lcb_destroy_callback);
void lcb_destroy_async(lcb_t instance, const void *arg);
typedef enum {
LCB_IO_OPS_INVALID=0,
LCB_IO_OPS_DEFAULT=1,
LCB_IO_OPS_LIBEVENT=2,
LCB_IO_OPS_WINSOCK=3,
LCB_IO_OPS_LIBEV=4,
LCB_IO_OPS_SELECT=5,
LCB_IO_OPS_WINIOCP=6,
LCB_IO_OPS_LIBUV=7,
} lcb_io_ops_type_t;
typedef struct {
    lcb_io_ops_type_t type;
    void *cookie;
} lcb_IOCREATEOPTS_BUILTIN;
typedef struct {
    const char *sofile;
    const char *symbol;
    void *cookie;
} lcb_IOCREATEOPTS_DSO;
typedef struct {
    lcb_io_create_fn create;
    void *cookie;
} lcb_IOCREATEOPS_FUNCTIONPOINTER;
struct lcb_create_io_ops_st {
    int version;
    union {
        lcb_IOCREATEOPTS_BUILTIN v0;
        lcb_IOCREATEOPTS_DSO v1;
        lcb_IOCREATEOPS_FUNCTIONPOINTER v2;
    } v;
};
lcb_error_t lcb_create_io_ops(lcb_io_opt_t *op,
                              const struct lcb_create_io_ops_st *options);
lcb_error_t lcb_destroy_io_ops(lcb_io_opt_t op);
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_time_t exptime;
    int lock;
    const void *hashkey; lcb_SIZE nhashkey;
} lcb_GETCMDv0;
typedef struct lcb_get_cmd_st {
    int version;
    union {
        lcb_GETCMDv0 v0;
    } v;
} lcb_get_cmd_t;
typedef enum {
LCB_VALUE_RAW=0,
LCB_VALUE_F_JSON=1,
LCB_VALUE_F_SNAPPYCOMP=2,
} lcb_VALUEFLAGS;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    const void *bytes;
    lcb_SIZE nbytes;
    lcb_U32 flags;
    lcb_cas_t cas;
    lcb_U8 datatype;
} lcb_GETRESPv0;
typedef struct {
    int version;
    union {
        lcb_GETRESPv0 v0;
    } v;
} lcb_get_resp_t;
typedef void (*lcb_get_callback)(lcb_t instance,
                                 const void *cookie,
                                 lcb_error_t error,
                                 const lcb_get_resp_t *resp);
lcb_get_callback lcb_set_get_callback(lcb_t, lcb_get_callback callback);
lcb_error_t lcb_get(lcb_t instance,
                    const void *command_cookie,
                    lcb_SIZE num,
                    const lcb_get_cmd_t *const *commands);
typedef struct { const void *key; lcb_SIZE nkey; const void *hashkey; lcb_SIZE nhashkey; } lcb_GETREPLICACMDv0;
typedef enum {
LCB_REPLICA_FIRST=0,
LCB_REPLICA_ALL=1,
LCB_REPLICA_SELECT=2,
} lcb_replica_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    const void *hashkey; lcb_SIZE nhashkey;
    lcb_replica_t strategy;
    int index;
} lcb_GETREPLICACMDv1;
typedef struct lcb_get_replica_cmd_st {
    int version;
    union {
        lcb_GETREPLICACMDv0 v0;
        lcb_GETREPLICACMDv1 v1;
    } v;
} lcb_get_replica_cmd_t;
lcb_error_t lcb_get_replica(lcb_t instance,
                            const void *command_cookie,
                            lcb_SIZE num,
                            const lcb_get_replica_cmd_t *const *commands);
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_cas_t cas;
    const void *hashkey; lcb_SIZE nhashkey;
} lcb_UNLOCKCMDv0;
typedef struct lcb_unlock_cmd_st {
    int version;
    union {
        lcb_UNLOCKCMDv0 v0;
    } v;
} lcb_unlock_cmd_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
} lcb_UNLOCKRESPv0;
typedef struct {
    int version;
    union {
        lcb_UNLOCKRESPv0 v0;
    } v;
} lcb_unlock_resp_t;
typedef void (*lcb_unlock_callback)(lcb_t instance,
                                    const void *cookie,
                                    lcb_error_t error,
                                    const lcb_unlock_resp_t *resp);
lcb_unlock_callback lcb_set_unlock_callback(lcb_t, lcb_unlock_callback);
lcb_error_t lcb_unlock(lcb_t instance,
                       const void *command_cookie,
                       lcb_SIZE num,
                       const lcb_unlock_cmd_t *const *commands);
typedef enum {
LCB_ADD=1,
LCB_REPLACE=2,
LCB_SET=3,
LCB_APPEND=4,
LCB_PREPEND=5,
} lcb_storage_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    const void *bytes;
    lcb_SIZE nbytes;
    lcb_U32 flags;
    lcb_cas_t cas;
    lcb_U8 datatype;
    lcb_time_t exptime;
    lcb_storage_t operation;
    const void *hashkey; lcb_SIZE nhashkey;
} lcb_STORECMDv0;
typedef struct lcb_store_cmd_st {
    int version;
    union {
        lcb_STORECMDv0 v0;
    } v;
} lcb_store_cmd_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_cas_t cas;
} lcb_STORERESPv0;
typedef struct {
    int version;
    union {
        lcb_STORERESPv0 v0;
    } v;
} lcb_store_resp_t;
typedef void (*lcb_store_callback)(lcb_t instance,
                                   const void *cookie,
                                   lcb_storage_t operation,
                                   lcb_error_t error,
                                   const lcb_store_resp_t *resp);
lcb_store_callback lcb_set_store_callback(lcb_t, lcb_store_callback callback);
lcb_error_t lcb_store(lcb_t instance,
                      const void *command_cookie,
                      lcb_SIZE num,
                      const lcb_store_cmd_t *const *commands);
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_time_t exptime;
    int create;
    lcb_S64 delta;
    lcb_U64 initial;
    const void *hashkey; lcb_SIZE nhashkey;
} lcb_ARITHCMDv0;
typedef struct lcb_arithmetic_cmd_st {
    int version;
    union {
        lcb_ARITHCMDv0 v0;
    } v;
} lcb_arithmetic_cmd_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_U64 value;
    lcb_cas_t cas;
} lcb_ARITHRESPv0;
typedef struct {
    int version;
    union {
        lcb_ARITHRESPv0 v0;
    } v;
} lcb_arithmetic_resp_t;
typedef void (*lcb_arithmetic_callback)(lcb_t instance,
                                        const void *cookie,
                                        lcb_error_t error,
                                        const lcb_arithmetic_resp_t *resp);
lcb_arithmetic_callback lcb_set_arithmetic_callback(lcb_t,
                                                    lcb_arithmetic_callback);
lcb_error_t lcb_arithmetic(lcb_t instance,
                           const void *command_cookie,
                           lcb_SIZE num,
                           const lcb_arithmetic_cmd_t *const *commands);
typedef enum {
LCB_OBSERVE_MASTER_ONLY=1,
} lcb_observe_options_t;
typedef struct {
    const void *key; lcb_SIZE nkey; const void *hashkey; lcb_SIZE nhashkey;
} lcb_OBSERVECMDv0;
typedef struct {
    const void *key; lcb_SIZE nkey; const void *hashkey; lcb_SIZE nhashkey;
    lcb_observe_options_t options;
} lcb_OBSERVECMDv1;
typedef struct lcb_observe_cmd_st {
    int version;
    union {
        lcb_OBSERVECMDv0 v0;
        lcb_OBSERVECMDv1 v1;
    } v;
} lcb_observe_cmd_t;
typedef enum {
LCB_OBSERVE_FOUND=0,
LCB_OBSERVE_PERSISTED=1,
LCB_OBSERVE_NOT_FOUND=128,
LCB_OBSERVE_LOGICALLY_DELETED=129,
LCB_OBSERVE_MAX=130,
} lcb_observe_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_cas_t cas;
    lcb_observe_t status;
    int from_master;
    lcb_time_t ttp;
    lcb_time_t ttr;
} lcb_OBSERVERESPv0;
typedef struct {
    int version;
    union {
        lcb_OBSERVERESPv0 v0;
    } v;
} lcb_observe_resp_t;
typedef void (*lcb_observe_callback)(lcb_t instance,
                                     const void *cookie,
                                     lcb_error_t error,
                                     const lcb_observe_resp_t *resp);
lcb_observe_callback lcb_set_observe_callback(lcb_t, lcb_observe_callback);
lcb_error_t lcb_observe(lcb_t instance,
                        const void *command_cookie,
                        lcb_SIZE num,
                        const lcb_observe_cmd_t *const *commands);
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_cas_t cas;
    const void *hashkey; lcb_SIZE nhashkey;
} lcb_REMOVECMDv0;
typedef struct lcb_remove_cmd_st {
    int version;
    union {
        lcb_REMOVECMDv0 v0;
    } v;
} lcb_remove_cmd_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_cas_t cas;
} lcb_REMOVERESPv0;
typedef struct {
    int version;
    union {
        lcb_REMOVERESPv0 v0;
    } v;
} lcb_remove_resp_t;
typedef void (*lcb_remove_callback)(lcb_t instance,
                                    const void *cookie,
                                    lcb_error_t error,
                                    const lcb_remove_resp_t *resp);
lcb_remove_callback lcb_set_remove_callback(lcb_t, lcb_remove_callback);
lcb_error_t lcb_remove(lcb_t instance,
                       const void *command_cookie,
                       lcb_SIZE num,
                       const lcb_remove_cmd_t *const *commands);
typedef lcb_get_cmd_t lcb_touch_cmd_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_cas_t cas;
} lcb_TOUCHRESPv0;
typedef struct {
    int version;
    union {
        lcb_TOUCHRESPv0 v0;
    } v;
} lcb_touch_resp_t;
typedef void (*lcb_touch_callback)(lcb_t instance,
                                   const void *cookie,
                                   lcb_error_t error,
                                   const lcb_touch_resp_t *resp);
lcb_touch_callback lcb_set_touch_callback(lcb_t, lcb_touch_callback);
lcb_error_t lcb_touch(lcb_t instance,
                      const void *cookie,
                      lcb_SIZE num,
                      const lcb_touch_cmd_t *const *commands);
typedef struct {
    const void *key;
    size_t nkey;
    const void *hashkey; lcb_SIZE nhashkey;
    lcb_cas_t cas;
} lcb_DURABILITYCMDv0;
typedef struct lcb_durability_cmd_st {
    int version;
    union {
        lcb_DURABILITYCMDv0 v0;
    } v;
} lcb_durability_cmd_t;
typedef struct {
    lcb_U32 timeout;
    lcb_U32 interval;
    lcb_U16 persist_to;
    lcb_U16 replicate_to;
    lcb_U8 check_delete;
    lcb_U8 cap_max;
} lcb_DURABILITYOPTSv0;
typedef struct lcb_durability_opts_st {
    int version;
    union {
        lcb_DURABILITYOPTSv0 v0;
    } v;
} lcb_durability_opts_t;
typedef struct {
    const void *key;
    lcb_SIZE nkey;
    lcb_error_t err;
    lcb_cas_t cas;
    unsigned char persisted_master;
    unsigned char exists_master;
    unsigned char npersisted;
    unsigned char nreplicated;
    unsigned short nresponses;
} lcb_DURABILITYRESPv0;
typedef struct lcb_durability_resp_st {
    int version;
    union {
        lcb_DURABILITYRESPv0 v0;
    } v;
} lcb_durability_resp_t;
lcb_error_t lcb_durability_poll(lcb_t instance,
                                const void *cookie,
                                const lcb_durability_opts_t *options,
                                lcb_SIZE ncmds,
                                const lcb_durability_cmd_t *const *cmds);
typedef void (*lcb_durability_callback)(lcb_t instance,
                                        const void *cookie,
                                        lcb_error_t err,
                                        const lcb_durability_resp_t *res);
lcb_durability_callback lcb_set_durability_callback(lcb_t,
                                                    lcb_durability_callback);
typedef struct {
    const void *name;
    lcb_SIZE nname;
} lcb_STATSCMDv0;
typedef struct lcb_server_stats_cmd_st {
    int version;
    union {
        lcb_STATSCMDv0 v0;
    } v;
} lcb_server_stats_cmd_t;
typedef struct {
    const char *server_endpoint;
    const void *key;
    lcb_SIZE nkey;
    const void *bytes;
    lcb_SIZE nbytes;
} lcb_STATSRESPv0;
typedef struct lcb_server_stat_resp_st {
    int version;
    union {
        lcb_STATSRESPv0 v0;
    } v;
} lcb_server_stat_resp_t;
typedef void (*lcb_stat_callback)(lcb_t instance,
                                  const void *cookie,
                                  lcb_error_t error,
                                  const lcb_server_stat_resp_t *resp);
lcb_stat_callback lcb_set_stat_callback(lcb_t, lcb_stat_callback);
lcb_error_t lcb_server_stats(lcb_t instance,
                             const void *command_cookie,
                             lcb_SIZE num,
                             const lcb_server_stats_cmd_t *const *commands);
typedef struct lcb_server_version_cmd_st {
    int version;
    union { struct { const void *notused; } v0; } v;
} lcb_server_version_cmd_t;
typedef struct lcb_server_version_resp_st {
    int version;
    union {
        struct {
            const char *server_endpoint;
            const char *vstring;
            lcb_SIZE nvstring;
        } v0;
    } v;
} lcb_server_version_resp_t;
lcb_error_t lcb_server_versions(lcb_t instance,
                                const void *command_cookie,
                                lcb_SIZE num,
                                const lcb_server_version_cmd_t *const *commands);
typedef void (*lcb_version_callback)(lcb_t instance,
                                     const void *cookie,
                                     lcb_error_t error,
                                     const lcb_server_version_resp_t *resp);
lcb_version_callback lcb_set_version_callback(lcb_t, lcb_version_callback);
typedef enum {
LCB_VERBOSITY_DETAIL=0,
LCB_VERBOSITY_DEBUG=1,
LCB_VERBOSITY_INFO=2,
LCB_VERBOSITY_WARNING=3,
} lcb_verbosity_level_t;
typedef struct {
    const char *server;
    lcb_verbosity_level_t level;
} lcb_VERBOSITYCMDv0;
typedef struct lcb_verbosity_cmd_st {
    int version;
    union {
        lcb_VERBOSITYCMDv0 v0;
    } v;
} lcb_verbosity_cmd_t;
typedef struct lcb_verbosity_resp_st {
    int version;
    union {
        struct {
            const char *server_endpoint;
        } v0;
    } v;
} lcb_verbosity_resp_t;
lcb_error_t lcb_set_verbosity(lcb_t instance,
                              const void *command_cookie,
                              lcb_SIZE num,
                              const lcb_verbosity_cmd_t *const *commands);
typedef void (*lcb_verbosity_callback)(lcb_t instance,
                                       const void *cookie,
                                       lcb_error_t error,
                                       const lcb_verbosity_resp_t *resp);
lcb_verbosity_callback lcb_set_verbosity_callback(lcb_t,
                                                  lcb_verbosity_callback);
typedef struct lcb_flush_cmd_st {
    int version;
    union { struct { int unused; } v0; } v;
} lcb_flush_cmd_t;
typedef struct lcb_flush_resp_st {
    int version;
    union {
        struct {
            const char *server_endpoint;
        } v0;
    } v;
} lcb_flush_resp_t;
lcb_error_t lcb_flush(lcb_t instance, const void *cookie,
                      lcb_SIZE num,
                      const lcb_flush_cmd_t *const *commands);
typedef void (*lcb_flush_callback)(lcb_t instance,
                                   const void *cookie,
                                   lcb_error_t error,
                                   const lcb_flush_resp_t *resp);
lcb_flush_callback lcb_set_flush_callback(lcb_t, lcb_flush_callback);
typedef enum {
LCB_HTTP_TYPE_VIEW=0,
LCB_HTTP_TYPE_MANAGEMENT=1,
LCB_HTTP_TYPE_RAW=2,
LCB_HTTP_TYPE_MAX=3,
} lcb_http_type_t;
typedef enum {
LCB_HTTP_METHOD_GET=0,
LCB_HTTP_METHOD_POST=1,
LCB_HTTP_METHOD_PUT=2,
LCB_HTTP_METHOD_DELETE=3,
LCB_HTTP_METHOD_MAX=4,
} lcb_http_method_t;
typedef struct {
    const char *path;
    lcb_SIZE npath;
    const void *body;
    lcb_SIZE nbody;
    lcb_http_method_t method;
    int chunked;
    const char *content_type;
} lcb_HTTPCMDv0;
typedef struct {
    const char *path;
    lcb_SIZE npath;
    const void *body;
    lcb_SIZE nbody;
    lcb_http_method_t method;
    int chunked;
    const char *content_type;
    const char *host;
    const char *username;
    const char *password;
} lcb_HTTPCMDv1;
typedef struct lcb_http_cmd_st {
    int version;
    union {
        lcb_HTTPCMDv0 v0;
        lcb_HTTPCMDv1 v1;
    } v;
} lcb_http_cmd_t;
typedef struct {
    lcb_http_status_t status;
    const char *path;
    lcb_SIZE npath;
    const char *const *headers;
    const void *bytes;
    lcb_SIZE nbytes;
} lcb_HTTPRESPv0;
typedef struct {
    int version;
    union {
        lcb_HTTPRESPv0 v0;
    } v;
} lcb_http_resp_t;
typedef void (*lcb_http_res_callback)(
        lcb_http_request_t request, lcb_t instance, const void *cookie,
        lcb_error_t error, const lcb_http_resp_t *resp);
typedef lcb_http_res_callback lcb_http_data_callback;
typedef lcb_http_res_callback lcb_http_complete_callback;
lcb_http_complete_callback
lcb_set_http_complete_callback(lcb_t, lcb_http_complete_callback);
lcb_http_data_callback
lcb_set_http_data_callback(lcb_t, lcb_http_data_callback);
lcb_error_t lcb_make_http_request(lcb_t instance,
                                  const void *command_cookie,
                                  lcb_http_type_t type,
                                  const lcb_http_cmd_t *cmd,
                                  lcb_http_request_t *request);
void lcb_cancel_http_request(lcb_t instance,
                             lcb_http_request_t request);
typedef enum {
LCB_NODE_HTCONFIG=1,
LCB_NODE_DATA=2,
LCB_NODE_VIEWS=4,
LCB_NODE_CONNECTED=8,
LCB_NODE_NEVERNULL=16,
LCB_NODE_HTCONFIG_CONNECTED=9,
LCB_NODE_HTCONFIG_ANY=17,
} lcb_GETNODETYPE;
const char *
lcb_get_node(lcb_t instance, lcb_GETNODETYPE type, unsigned index);
lcb_S32 lcb_get_num_replicas(lcb_t instance);
lcb_S32 lcb_get_num_nodes(lcb_t instance);
const char *const *lcb_get_server_list(lcb_t instance);
int lcb_is_waiting(lcb_t instance);
lcb_error_t lcb_cntl(lcb_t instance, int mode, int cmd, void *arg);
lcb_error_t
lcb_cntl_string(lcb_t instance, const char *key, const char *value);
lcb_error_t lcb_cntl_setu32(lcb_t instance, int cmd, lcb_U32 arg);
lcb_U32 lcb_cntl_getu32(lcb_t instance, int cmd);
int
lcb_cntl_exists(int ctl);
enum lcb_timeunit_t {
LCB_TIMEUNIT_NSEC=0,
LCB_TIMEUNIT_USEC=1,
LCB_TIMEUNIT_MSEC=2,
LCB_TIMEUNIT_SEC=3,
};
typedef enum lcb_timeunit_t lcb_timeunit_t;
lcb_error_t lcb_enable_timings(lcb_t instance);
lcb_error_t lcb_disable_timings(lcb_t instance);
typedef void (*lcb_timings_callback)(lcb_t instance,
                                     const void *cookie,
                                     lcb_timeunit_t timeunit,
                                     lcb_U32 min,
                                     lcb_U32 max,
                                     lcb_U32 total,
                                     lcb_U32 maxtotal);
lcb_error_t lcb_get_timings(lcb_t instance,
                            const void *cookie,
                            lcb_timings_callback callback);
const char *lcb_get_version(lcb_U32 *version);
int
lcb_supports_feature(int n);
lcb_error_t lcb_errmap_default(lcb_t instance, lcb_U16 code);
typedef lcb_error_t (*lcb_errmap_callback)(lcb_t instance, lcb_U16 bincode);
lcb_errmap_callback lcb_set_errmap_callback(lcb_t, lcb_errmap_callback);
void *lcb_mem_alloc(lcb_SIZE size);
void lcb_mem_free(void *ptr);
void lcb_run_loop(lcb_t instance);
void lcb_stop_loop(lcb_t instance);
typedef enum {
LCB_DUMP_VBCONFIG=1,
LCB_DUMP_PKTINFO=2,
LCB_DUMP_BUFINFO=4,
LCB_DUMP_ALL=255,
} lcb_DUMPFLAGS;
void
lcb_dump(lcb_t instance, FILE *fp, lcb_U32 flags);
typedef struct lcb_cntl_vbinfo_st {
    int version;
    union {
        struct {
            const void *key;
            lcb_SIZE nkey;
            int vbucket;
            int server_index;
        } v0;
    } v;
} lcb_cntl_vbinfo_t;
typedef enum {LCB_LOG_TRACE=0, LCB_LOG_DEBUG, LCB_LOG_INFO, LCB_LOG_WARN,
    LCB_LOG_ERROR, LCB_LOG_FATAL, LCB_LOG_MAX
} lcb_log_severity_t;
struct lcb_logprocs_st;
typedef void (*lcb_logging_callback)(struct lcb_logprocs_st *procs,
        unsigned int iid, const char *subsys, int severity, const char *srcfile,
        int srcline, const char *fmt, va_list ap);
typedef struct lcb_logprocs_st {
    int version;
    union { struct { lcb_logging_callback callback; } v0; } v;
} lcb_logprocs;
typedef enum {
LCB_SSL_ENABLED=1,
LCB_SSL_NOVERIFY=2,
} lcb_SSLOPTS;
typedef enum {
LCB_RETRY_ON_TOPOCHANGE=0,
    LCB_RETRY_ON_SOCKERR,
    LCB_RETRY_ON_VBMAPERR,
    LCB_RETRY_ON_MISSINGNODE,
    LCB_RETRY_ON_MAX
} lcb_RETRYMODEOPTS;
typedef enum {
LCB_RETRY_CMDS_NONE=0,
LCB_RETRY_CMDS_GET=1,
LCB_RETRY_CMDS_SAFE=3,
LCB_RETRY_CMDS_ALL=3,
} lcb_RETRYCMDOPTS;
typedef enum {
LCB_HTCONFIG_URLTYPE_25PLUS=1,
LCB_HTCONFIG_URLTYPE_COMPAT=2,
LCB_HTCONFIG_URLTYPE_TRYALL=3,
} lcb_HTCONFIG_URLTYPE;
typedef struct lcb_cntl_server_st {
    int version;
    union {
        struct {
            int index; const char *host; const char *port; int connected; union { lcb_socket_t sockfd; lcb_sockdata_t *sockptr; } sock;
        } v0;
        struct {
            int index; const char *host; const char *port; int connected; union { lcb_socket_t sockfd; lcb_sockdata_t *sockptr; } sock;
            const char *sasl_mech;
        } v1;
    } v;
} lcb_cntl_server_t;
struct lcb_cntl_iops_info_st {
    int version;
    union {
        struct {
            const struct lcb_create_io_ops_st *options;
            lcb_io_ops_type_t os_default;
            lcb_io_ops_type_t effective;
        } v0;
    } v;
};
typedef enum {
LCB_COMPRESS_NONE=0,
LCB_COMPRESS_IN=1,
LCB_COMPRESS_OUT=2,
LCB_COMPRESS_INOUT=3,
LCB_COMPRESS_FORCE=4,
} lcb_COMPRESSOPTS;
struct rdb_ALLOCATOR;
typedef struct rdb_ALLOCATOR* (*lcb_RDBALLOCFACTORY)(void);
struct lcb_cntl_rdballocfactory {
    lcb_RDBALLOCFACTORY factory;
};
typedef enum {
LCB_IPV6_DISABLED=0,LCB_IPV6_ONLY=1,LCB_IPV6_ALLOW=2,
} lcb_ipv6_t;
typedef enum {
LCB_KV_COPY=0,
    LCB_KV_CONTIG,
    LCB_KV_IOV
} lcb_KVBUFTYPE;
typedef struct lcb_CONTIGBUF {
    const void *bytes;
    lcb_size_t nbytes;
} lcb_CONTIGBUF;
typedef struct lcb_KEYBUF {
    lcb_KVBUFTYPE type;
    lcb_CONTIGBUF contig;
} lcb_KEYBUF;
typedef struct lcb_FRAGBUF {
    lcb_IOV *iov;
    unsigned int niov;
    unsigned int total_length;
} lcb_FRAGBUF;
typedef struct lcb_VALBUF {
    lcb_KVBUFTYPE vtype;
    union {
        lcb_CONTIGBUF contig;
        lcb_FRAGBUF multi;
    } u_buf;
} lcb_VALBUF;
typedef struct lcb_CMDBASE {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
} lcb_CMDBASE;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
} lcb_RESPBASE;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    const char *server;
} lcb_RESPSERVERBASE;
typedef enum {
LCB_RESP_F_FINAL=1,
LCB_RESP_F_CLIENTGEN=2,
LCB_RESP_F_NMVGEN=4,
} lcb_RESPFLAGS;
typedef enum {
LCB_CALLBACK_DEFAULT=0,
    LCB_CALLBACK_GET,
    LCB_CALLBACK_STORE,
    LCB_CALLBACK_COUNTER,
    LCB_CALLBACK_TOUCH,
    LCB_CALLBACK_REMOVE,
    LCB_CALLBACK_UNLOCK,
    LCB_CALLBACK_STATS,
    LCB_CALLBACK_VERSIONS,
    LCB_CALLBACK_VERBOSITY,
    LCB_CALLBACK_FLUSH,
    LCB_CALLBACK_OBSERVE,
    LCB_CALLBACK_GETREPLICA,
    LCB_CALLBACK_ENDURE,
    LCB_CALLBACK_HTTP,
    LCB_CALLBACK__MAX
} lcb_CALLBACKTYPE;
typedef void (*lcb_RESPCALLBACK)
        (lcb_t instance, int cbtype, const lcb_RESPBASE* resp);
lcb_RESPCALLBACK
lcb_install_callback3(lcb_t instance, int cbtype, lcb_RESPCALLBACK cb);
void lcb_sched_enter(lcb_t instance);
void lcb_sched_leave(lcb_t instance);
void lcb_sched_fail(lcb_t instance);
typedef struct {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
    int lock;
} lcb_CMDGET;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    const void *value;
    lcb_SIZE nvalue;
    void* bufh;
    lcb_datatype_t datatype;
    lcb_U32 itmflags;
} lcb_RESPGET;
lcb_error_t
lcb_get3(lcb_t instance, const void *cookie, const lcb_CMDGET *cmd);
typedef lcb_CMDBASE lcb_CMDUNLOCK;
typedef lcb_RESPBASE lcb_RESPUNLOCK;
lcb_error_t
lcb_unlock3(lcb_t instance, const void *cookie, const lcb_CMDUNLOCK *cmd);
typedef struct {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
    lcb_int64_t delta;
    lcb_U64 initial;
    int create;
} lcb_CMDCOUNTER;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    lcb_U64 value;
} lcb_RESPCOUNTER;
lcb_error_t
lcb_counter3(lcb_t instance, const void *cookie, const lcb_CMDCOUNTER *cmd);
typedef struct {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
    lcb_replica_t strategy;
    int index;
} lcb_CMDGETREPLICA;
lcb_error_t
lcb_rget3(lcb_t instance, const void *cookie, const lcb_CMDGETREPLICA *cmd);
typedef struct {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
    lcb_VALBUF value;
    lcb_U32 flags;
    lcb_datatype_t datatype;
    lcb_storage_t operation;
} lcb_CMDSTORE;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    lcb_storage_t op;
} lcb_RESPSTORE;
lcb_error_t
lcb_store3(lcb_t instance, const void *cookie, const lcb_CMDSTORE *cmd);
typedef lcb_CMDBASE lcb_CMDREMOVE;
typedef lcb_RESPBASE lcb_RESPREMOVE;
lcb_error_t
lcb_remove3(lcb_t instance, const void *cookie, const lcb_CMDREMOVE * cmd);
typedef lcb_CMDBASE lcb_CMDTOUCH;
typedef lcb_RESPBASE lcb_RESPTOUCH;
lcb_error_t
lcb_touch3(lcb_t instance, const void *cookie, const lcb_CMDTOUCH *cmd);
typedef lcb_CMDBASE lcb_CMDSTATS;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    const char *server;
    const char *value;
    lcb_SIZE nvalue;
} lcb_RESPSTATS;
lcb_error_t
lcb_stats3(lcb_t instance, const void *cookie, const lcb_CMDSTATS * cmd);
typedef struct lcb_MULTICMD_CTX_st {
    lcb_error_t (*addcmd)(struct lcb_MULTICMD_CTX_st *ctx, const lcb_CMDBASE *cmd);
    lcb_error_t (*done)(struct lcb_MULTICMD_CTX_st *ctx, const void *cookie);
    void (*fail)(struct lcb_MULTICMD_CTX_st *ctx);
} lcb_MULTICMD_CTX;
typedef lcb_CMDBASE lcb_CMDOBSERVE;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    lcb_U8 status;
    lcb_U8 ismaster;
    lcb_U32 ttp;
    lcb_U32 ttr;
} lcb_RESPOBSERVE;
lcb_MULTICMD_CTX *
lcb_observe3_ctxnew(lcb_t instance);
typedef lcb_CMDBASE lcb_CMDENDURE;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    lcb_U16 nresponses;
    lcb_U8 exists_master;
    lcb_U8 persisted_master;
    lcb_U8 npersisted;
    lcb_U8 nreplicated;
} lcb_RESPENDURE;
lcb_MULTICMD_CTX *
lcb_endure3_ctxnew(lcb_t instance,
    const lcb_durability_opts_t *options, lcb_error_t *err);
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    const char *server;
    const char *mcversion;
    lcb_SIZE nversion;
} lcb_RESPMCVERSION;
lcb_error_t
lcb_server_versions3(lcb_t instance, const void *cookie, const lcb_CMDBASE * cmd);
typedef struct {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
    const char *server;
    lcb_verbosity_level_t level;
} lcb_CMDVERBOSITY;
typedef lcb_RESPSERVERBASE lcb_RESPVERBOSITY;
lcb_error_t
lcb_server_verbosity3(lcb_t instance, const void *cookie, const lcb_CMDVERBOSITY *cmd);
typedef lcb_CMDBASE lcb_CMDFLUSH;
typedef lcb_RESPSERVERBASE lcb_RESPFLUSH;
lcb_error_t
lcb_flush3(lcb_t instance, const void *cookie, const lcb_CMDFLUSH *cmd);
typedef struct {
    lcb_U32 cmdflags; lcb_U32 exptime; lcb_U64 cas; lcb_KEYBUF key; lcb_KEYBUF _hashkey;
    lcb_http_type_t type;
    lcb_http_method_t method;
    const char *body;
    lcb_SIZE nbody;
    lcb_http_request_t *reqhandle;
    const char *content_type;
    const char *username;
    const char *password;
    const char *host;
} lcb_CMDHTTP;
typedef struct {
    void *cookie; const void *key; lcb_SIZE nkey; lcb_cas_t cas; lcb_error_t rc; lcb_U16 version; lcb_U16 rflags;
    short htstatus;
    const char * const * headers;
    const void *body;
    lcb_SIZE nbody;
    lcb_http_request_t _htreq;
} lcb_RESPHTTP;
lcb_error_t
lcb_http3(lcb_t instance, const void *cookie, const lcb_CMDHTTP *cmd);
 void lcb_behavior_set_ipv6(lcb_t instance, lcb_ipv6_t mode) ; lcb_ipv6_t lcb_behavior_get_ipv6(lcb_t instance) ; void lcb_behavior_set_config_errors_threshold(lcb_t instance, lcb_size_t num_events) ; lcb_size_t lcb_behavior_get_config_errors_threshold(lcb_t instance) ; void lcb_set_timeout(lcb_t instance, lcb_uint32_t usec) ; lcb_uint32_t lcb_get_timeout(lcb_t instance) ; void lcb_set_view_timeout(lcb_t instance, lcb_uint32_t usec) ; lcb_uint32_t lcb_get_view_timeout(lcb_t instance) ; lcb_error_t lcb_get_last_error(lcb_t instance) ; void lcb_flush_buffers(lcb_t instance, const void *cookie) ;
typedef enum {
LCB_VBUCKET_STATE_ACTIVE=1,
LCB_VBUCKET_STATE_REPLICA=2,
LCB_VBUCKET_STATE_PENDING=3,
LCB_VBUCKET_STATE_DEAD=4,
} lcb_vbucket_state_t;
typedef void (*lcb_error_callback)(lcb_t instance, lcb_error_t error, const char *errinfo); lcb_error_callback lcb_set_error_callback(lcb_t, lcb_error_callback) ;
struct lcb_timer_st;
typedef struct lcb_timer_st *lcb_timer_t;
typedef void (*lcb_timer_callback)(lcb_timer_t timer, lcb_t instance, const void *cookie); lcb_timer_t lcb_timer_create(lcb_t instance, const void *command_cookie, lcb_uint32_t usec, int periodic, lcb_timer_callback callback, lcb_error_t *error) ; lcb_error_t lcb_timer_destroy(lcb_t instance, lcb_timer_t timer) ;
typedef enum lcb_compat_t {LCB_MEMCACHED_CLUSTER=0,LCB_CACHED_CONFIG=1} lcb_compat_t;
typedef lcb_compat_t lcb_cluster_t;
struct lcb_memcached_st { const char *serverlist; const char *username; const char *password; };
struct lcb_cached_config_st {
    const char *cachefile;
    struct lcb_create_st createopt;
}; lcb_error_t lcb__create_compat_230(lcb_compat_t type, const void *specific, lcb_t *instance, struct lcb_io_opt_st *io) ;
typedef enum {
LCB_ASYNCHRONOUS=0,
LCB_SYNCHRONOUS=255,
} lcb_syncmode_t; void lcb_behavior_set_syncmode(lcb_t, lcb_syncmode_t) ; lcb_syncmode_t lcb_behavior_get_syncmode(lcb_t) ; const char *lcb_get_host(lcb_t) ; const char *lcb_get_port(lcb_t) ;
typedef enum {
LCB_C_ST_ID=0,LCB_C_ST_V=3,LCB_C_I_O_ST_ID=1,LCB_C_I_O_ST_V=1,LCB_G_C_ST_ID=2,LCB_G_C_ST_V=0,LCB_G_R_C_ST_ID=3,LCB_G_R_C_ST_V=1,LCB_U_C_ST_ID=4,LCB_U_C_ST_V=0,LCB_T_C_ST_ID=5,LCB_T_C_ST_V=0,LCB_S_C_ST_ID=6,LCB_S_C_ST_V=0,LCB_A_C_ST_ID=7,LCB_A_C_ST_V=0,LCB_O_C_ST_ID=8,LCB_O_C_ST_V=0,LCB_R_C_ST_ID=9,LCB_R_C_ST_V=0,LCB_H_C_ST_ID=10,LCB_H_C_ST_V=1,LCB_S_S_C_ST_ID=11,LCB_S_S_C_ST_V=0,LCB_S_V_C_ST_ID=12,LCB_S_V_C_ST_V=0,LCB_V_C_ST_ID=13,LCB_V_C_ST_V=0,LCB_F_C_ST_ID=14,LCB_F_C_ST_V=0,LCB_G_R_ST_ID=15,LCB_G_R_ST_V=0,LCB_S_R_ST_ID=16,LCB_S_R_ST_V=0,LCB_R_R_ST_ID=17,LCB_R_R_ST_V=0,LCB_T_R_ST_ID=18,LCB_T_R_ST_V=0,LCB_U_R_ST_ID=19,LCB_U_R_ST_V=0,LCB_A_R_ST_ID=20,LCB_A_R_ST_V=0,LCB_O_R_ST_ID=21,LCB_O_R_ST_V=0,LCB_H_R_ST_ID=22,LCB_H_R_ST_V=0,LCB_S_S_R_ST_ID=23,LCB_S_S_R_ST_V=0,LCB_S_V_R_ST_ID=24,LCB_S_V_R_ST_V=0,LCB_V_R_ST_ID=25,LCB_V_R_ST_V=0,LCB_F_R_ST_ID=26,LCB_F_R_ST_V=0,
LCB_ST_M=26,
} lcb__STRUCTSIZES;
lcb_error_t lcb_verify_struct_size(lcb_uint32_t id, lcb_uint32_t version,
                                   lcb_size_t size);
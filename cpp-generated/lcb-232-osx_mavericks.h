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
LCB_SUCCESS=0,LCB_AUTH_CONTINUE=1,LCB_AUTH_ERROR=2,LCB_DELTA_BADVAL=3,LCB_E2BIG=4,LCB_EBUSY=5,LCB_EINTERNAL=6,LCB_EINVAL=7,LCB_ENOMEM=8,LCB_ERANGE=9,LCB_ERROR=10,LCB_ETMPFAIL=11,LCB_KEY_EEXISTS=12,LCB_KEY_ENOENT=13,LCB_DLOPEN_FAILED=14,LCB_DLSYM_FAILED=15,LCB_NETWORK_ERROR=16,LCB_NOT_MY_VBUCKET=17,LCB_NOT_STORED=18,LCB_NOT_SUPPORTED=19,LCB_UNKNOWN_COMMAND=20,LCB_UNKNOWN_HOST=21,LCB_PROTOCOL_ERROR=22,LCB_ETIMEDOUT=23,LCB_CONNECT_ERROR=24,LCB_BUCKET_ENOENT=25,LCB_CLIENT_ENOMEM=26,LCB_CLIENT_ETMPFAIL=27,LCB_EBADHANDLE=28,LCB_SERVER_BUG=29,LCB_PLUGIN_VERSION_MISMATCH=30,LCB_INVALID_HOST_FORMAT=31,LCB_INVALID_CHAR=32,LCB_DURABILITY_ETOOMANY=33,LCB_DUPLICATE_COMMANDS=34,LCB_NO_MATCHING_SERVER=35,LCB_BAD_ENVIRONMENT=36,LCB_BUSY=37,LCB_INVALID_USERNAME=38,LCB_CONFIG_CACHE_INVALID=39,LCB_SASLMECH_UNAVAILABLE=40,LCB_TOO_MANY_REDIRECTS=41,
LCB_MAX_ERROR=4096,
    } lcb_error_t;
int lcb_get_errtype(lcb_error_t err);
    struct lcb_st;
    typedef struct lcb_st *lcb_t;
    struct lcb_http_request_st;
    typedef struct lcb_http_request_st *lcb_http_request_t;
    struct lcb_timer_st;
    typedef struct lcb_timer_st *lcb_timer_t;
    typedef lcb_uint8_t lcb_datatype_t;
    typedef enum {
LCB_CONFIGURATION_NEW=0,
LCB_CONFIGURATION_CHANGED=1,
LCB_CONFIGURATION_UNCHANGED=2,
    } lcb_configuration_t;
    typedef enum {
LCB_ADD=1,
LCB_REPLACE=2,
LCB_SET=3,
LCB_APPEND=4,
LCB_PREPEND=5,
    } lcb_storage_t;
    typedef enum {
LCB_OBSERVE_FOUND=0,
LCB_OBSERVE_PERSISTED=1,
LCB_OBSERVE_NOT_FOUND=128,
LCB_OBSERVE_LOGICALLY_DELETED=129,
LCB_OBSERVE_MAX=130,
    } lcb_observe_t;
    typedef enum {
LCB_TYPE_BUCKET=0,
LCB_TYPE_CLUSTER=1,
    } lcb_type_t;
    typedef int lcb_socket_t;
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
    typedef enum {
LCB_VBUCKET_STATE_ACTIVE=1,
LCB_VBUCKET_STATE_REPLICA=2,
LCB_VBUCKET_STATE_PENDING=3,
LCB_VBUCKET_STATE_DEAD=4,
    } lcb_vbucket_state_t;
    typedef enum {
LCB_VERBOSITY_DETAIL=0,
LCB_VERBOSITY_DEBUG=1,
LCB_VERBOSITY_INFO=2,
LCB_VERBOSITY_WARNING=3,
    } lcb_verbosity_level_t;
    struct sockaddr;
    struct lcb_iovec_st {
        char *iov_base;
        lcb_size_t iov_len;
    };
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
    typedef struct lcb_io_opt_st *lcb_io_opt_t;
    struct lcb_iops_table_v0_st {
        void *cookie;
        int error;
        int need_cleanup;
        lcb_socket_t (*socket)(struct lcb_io_opt_st *iops,
                               int domain,
                               int type,
                               int protocol);
        int (*connect)(struct lcb_io_opt_st *iops,
                       lcb_socket_t sock,
                       const struct sockaddr *name,
                       unsigned int namelen);
        lcb_ssize_t (*recv)(struct lcb_io_opt_st *iops,
                            lcb_socket_t sock,
                            void *buffer,
                            lcb_size_t len,
                            int flags);
        lcb_ssize_t (*send)(struct lcb_io_opt_st *iops,
                            lcb_socket_t sock,
                            const void *msg,
                            lcb_size_t len,
                            int flags);
        lcb_ssize_t (*recvv)(struct lcb_io_opt_st *iops,
                             lcb_socket_t sock,
                             struct lcb_iovec_st *iov,
                             lcb_size_t niov);
        lcb_ssize_t (*sendv)(struct lcb_io_opt_st *iops,
                             lcb_socket_t sock,
                             struct lcb_iovec_st *iov,
                             lcb_size_t niov);
        void (*close)(struct lcb_io_opt_st *iops,
                      lcb_socket_t sock);
        void *(*create_timer)(struct lcb_io_opt_st *iops);
        void (*destroy_timer)(struct lcb_io_opt_st *iops,
                              void *timer);
        void (*delete_timer)(struct lcb_io_opt_st *iops,
                             void *timer);
        int (*update_timer)(struct lcb_io_opt_st *iops,
                            void *timer,
                            lcb_uint32_t usec,
                            void *cb_data,
                            void (*handler)(lcb_socket_t sock,
                                            short which,
                                            void *cb_data));
        void *(*create_event)(struct lcb_io_opt_st *iops);
        void (*destroy_event)(struct lcb_io_opt_st *iops,
                              void *event);
        int (*update_event)(struct lcb_io_opt_st *iops,
                            lcb_socket_t sock,
                            void *event,
                            short flags,
                            void *cb_data,
                            void (*handler)(lcb_socket_t sock,
                                            short which,
                                            void *cb_data));
        void (*delete_event)(struct lcb_io_opt_st *iops,
                             lcb_socket_t sock,
                             void *event);
        void (*stop_event_loop)(struct lcb_io_opt_st *iops);
        void (*run_event_loop)(struct lcb_io_opt_st *iops);
    };
    struct ringbuffer_st;
    struct lcb_buf_info {
        char *root;
        lcb_size_t size;
        struct ringbuffer_st *ringbuffer;
        struct lcb_iovec_st iov[2];
    };
    struct lcb_connection_st;
    typedef struct lcb_sockdata_st {
        lcb_socket_t socket;
        lcb_io_opt_t parent;
        struct lcb_connection_st *lcbconn;
        int closed;
        int is_reading;
        struct lcb_buf_info read_buffer;
    } lcb_sockdata_t;
    typedef struct lcb_io_writebuf_st {
        struct lcb_io_opt_st *parent;
        struct lcb_buf_info buffer;
    } lcb_io_writebuf_t;
    typedef void (*lcb_io_v0_callback)(lcb_socket_t, short, void *);
    typedef void (*lcb_io_connect_cb)(lcb_sockdata_t *socket, int status);
    typedef void (*lcb_io_read_cb)(lcb_sockdata_t *socket, lcb_ssize_t nr);
    typedef void (*lcb_io_error_cb)(lcb_sockdata_t *socket);
    typedef void (*lcb_io_write_cb)(lcb_sockdata_t *socket,
                                    lcb_io_writebuf_t *buf,
                                    int status);
    struct lcb_iops_table_v1_st {
        void *cookie;
        int error;
        int need_cleanup;
        lcb_sockdata_t *(*create_socket)(struct lcb_io_opt_st *iops,
                                         int domain,
                                         int type,
                                         int protocol);
        int (*start_connect)(struct lcb_io_opt_st *iops,
                             lcb_sockdata_t *socket,
                             const struct sockaddr *name,
                             unsigned int namelen,
                             lcb_io_connect_cb callback);
        lcb_io_writebuf_t *(*create_writebuf)(struct lcb_io_opt_st *iops,
                                              lcb_sockdata_t *sock);
        void (*release_writebuf)(struct lcb_io_opt_st *iops,
                                 lcb_sockdata_t *sock,
                                 lcb_io_writebuf_t *buf);
        int (*start_write)(struct lcb_io_opt_st *iops,
                           lcb_sockdata_t *socket,
                           lcb_io_writebuf_t *buf,
                           lcb_io_write_cb callback);
        int (*start_read)(struct lcb_io_opt_st *iops,
                          lcb_sockdata_t *socket,
                          lcb_io_read_cb callback);
        unsigned int (*close_socket)(struct lcb_io_opt_st *iops,
                                     lcb_sockdata_t *socket);
        void *(*create_timer)(struct lcb_io_opt_st *iops);
        void (*destroy_timer)(struct lcb_io_opt_st *iops,
                              void *timer);
        void (*delete_timer)(struct lcb_io_opt_st *iops,
                             void *timer);
        int (*update_timer)(struct lcb_io_opt_st *iops,
                            void *timer,
                            lcb_uint32_t usec,
                            void *cb_data,
                            void (*handler)(lcb_socket_t sock,
                                            short which,
                                            void *cb_data));
        int (*get_nameinfo)(struct lcb_io_opt_st *iops,
                            lcb_sockdata_t *sock,
                            struct lcb_nameinfo_st *ni);
        void (*pad_2)(void);
        void (*pad_3)(void);
        void (*send_error)(struct lcb_io_opt_st *iops,
                           lcb_sockdata_t *sock,
                           lcb_io_error_cb callback);
        void (*stop_event_loop)(struct lcb_io_opt_st *iops);
        void (*run_event_loop)(struct lcb_io_opt_st *iops);
    };
    struct lcb_io_opt_st {
        int version;
        void *dlhandle;
        void (*destructor)(struct lcb_io_opt_st *iops);
        union {
            struct lcb_iops_table_v0_st v0;
            struct lcb_iops_table_v1_st v1;
        } v;
    };
    typedef enum {
LCB_ASYNCHRONOUS=0,
LCB_SYNCHRONOUS=255,
    } lcb_syncmode_t;
    typedef enum {
LCB_IPV6_DISABLED=0,
LCB_IPV6_ONLY=1,
LCB_IPV6_ALLOW=2,
    } lcb_ipv6_t;
    typedef enum {
LCB_LOG_TRACE=0,
        LCB_LOG_DEBUG,
        LCB_LOG_INFO,
        LCB_LOG_WARN,
        LCB_LOG_ERROR,
        LCB_LOG_FATAL,
        LCB_LOG_MAX
    } lcb_log_severity_t;
    struct lcb_logprocs_st;
    typedef void (*lcb_logging_callback)(struct lcb_logprocs_st *procs,
                                          unsigned int iid,
                                          const char *subsys,
                                          int severity,
                                          const char *srcfile,
                                          int srcline,
                                          const char *fmt,
                                          va_list ap);
    typedef struct lcb_logprocs_st {
        int version;
        union {
            struct {
                lcb_logging_callback callback;
            } v0;
        } v;
    } lcb_logprocs;
    typedef enum {
LCB_CONFIG_TRANSPORT_LIST_END=0,
LCB_CONFIG_TRANSPORT_HTTP=1,
        LCB_CONFIG_TRANSPORT_CCCP
    } lcb_config_transport_t;
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
    struct lcb_create_st0 {
        const char *host; const char *user; const char *passwd; const char *bucket; struct lcb_io_opt_st *io;
    };
    struct lcb_create_st1 {
        const char *host; const char *user; const char *passwd; const char *bucket; struct lcb_io_opt_st *io; lcb_type_t type;
    };
    struct lcb_create_st2 {
        const char *host; const char *user; const char *passwd; const char *bucket; struct lcb_io_opt_st *io; lcb_type_t type; const char *mchosts; const lcb_config_transport_t* transports;
    };
    struct lcb_create_st {
        int version;
        union {
            struct lcb_create_st0 v0;
            struct lcb_create_st1 v1;
            struct lcb_create_st2 v2;
        } v;
    };
    struct lcb_create_io_ops_st {
        int version;
        union {
            struct {
                lcb_io_ops_type_t type;
                void *cookie;
            } v0;
            struct {
                const char *sofile;
                const char *symbol;
                void *cookie;
            } v1;
            struct {
                lcb_error_t (*create)(int version,
                                      lcb_io_opt_t *io,
                                      void *cookie);
                void *cookie;
            } v2;
        } v;
    };
    typedef struct lcb_get_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_time_t exptime;
                int lock;
                const void *hashkey;
                lcb_size_t nhashkey;
            } v0;
        } v;
    } lcb_get_cmd_t;
    typedef enum {
LCB_REPLICA_FIRST=0,
LCB_REPLICA_ALL=1,
LCB_REPLICA_SELECT=2,
    } lcb_replica_t;
    typedef struct lcb_get_replica_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                const void *hashkey;
                lcb_size_t nhashkey;
            } v0;
            struct {
                const void *key;
                lcb_size_t nkey;
                const void *hashkey;
                lcb_size_t nhashkey;
                lcb_replica_t strategy;
                int index;
            } v1;
        } v;
    } lcb_get_replica_cmd_t;
    typedef struct lcb_unlock_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_cas_t cas;
                const void *hashkey;
                lcb_size_t nhashkey;
            } v0;
        } v;
    } lcb_unlock_cmd_t;
    typedef lcb_get_cmd_t lcb_touch_cmd_t;
    typedef struct lcb_store_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                const void *bytes;
                lcb_size_t nbytes;
                lcb_uint32_t flags;
                lcb_cas_t cas;
                lcb_datatype_t datatype;
                lcb_time_t exptime;
                lcb_storage_t operation;
                const void *hashkey;
                lcb_size_t nhashkey;
            } v0;
        } v;
    } lcb_store_cmd_t;
    typedef struct lcb_arithmetic_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_time_t exptime;
                int create;
                lcb_int64_t delta;
                lcb_uint64_t initial;
                const void *hashkey;
                lcb_size_t nhashkey;
            } v0;
        } v;
    } lcb_arithmetic_cmd_t;
    typedef enum {
LCB_OBSERVE_MASTER_ONLY=1,
    } lcb_observe_options_t;
    typedef struct lcb_observe_cmd_st {
        int version;
        union {
            struct {
                const void *key; lcb_size_t nkey; const void *hashkey; lcb_size_t nhashkey;
            } v0;
            struct {
                const void *key; lcb_size_t nkey; const void *hashkey; lcb_size_t nhashkey;
                lcb_observe_options_t options;
            } v1;
        } v;
    } lcb_observe_cmd_t;
    typedef struct lcb_remove_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_cas_t cas;
                const void *hashkey;
                lcb_size_t nhashkey;
            } v0;
        } v;
    } lcb_remove_cmd_t;
    typedef struct lcb_http_cmd_st {
        int version;
        union {
            struct {
                const char *path;
                lcb_size_t npath;
                const void *body;
                lcb_size_t nbody;
                lcb_http_method_t method;
                int chunked;
                const char *content_type;
            } v0;
            struct {
                const char *path;
                lcb_size_t npath;
                const void *body;
                lcb_size_t nbody;
                lcb_http_method_t method;
                int chunked;
                const char *content_type;
                const char *host;
                const char *username;
                const char *password;
            } v1;
        } v;
    } lcb_http_cmd_t;
    typedef struct lcb_server_stats_cmd_st {
        int version;
        union {
            struct {
                const void *name;
                lcb_size_t nname;
            } v0;
        } v;
    } lcb_server_stats_cmd_t;
    typedef struct lcb_server_version_cmd_st {
        int version;
        union {
            struct {
                const void *notused;
            } v0;
        } v;
    } lcb_server_version_cmd_t;
    typedef struct lcb_verbosity_cmd_st {
        int version;
        union {
            struct {
                const char *server;
                lcb_verbosity_level_t level;
            } v0;
        } v;
    } lcb_verbosity_cmd_t;
    typedef struct lcb_flush_cmd_st {
        int version;
        union {
            struct {
                int unused;
            } v0;
        } v;
    } lcb_flush_cmd_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                const void *bytes;
                lcb_size_t nbytes;
                lcb_uint32_t flags;
                lcb_cas_t cas;
                lcb_datatype_t datatype;
            } v0;
        } v;
    } lcb_get_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_cas_t cas;
            } v0;
        } v;
    } lcb_store_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_cas_t cas;
            } v0;
        } v;
    } lcb_remove_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_cas_t cas;
            } v0;
        } v;
    } lcb_touch_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
            } v0;
        } v;
    } lcb_unlock_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_uint64_t value;
                lcb_cas_t cas;
            } v0;
        } v;
    } lcb_arithmetic_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_cas_t cas;
                lcb_observe_t status;
                int from_master;
                lcb_time_t ttp;
                lcb_time_t ttr;
            } v0;
        } v;
    } lcb_observe_resp_t;
    typedef struct {
        int version;
        union {
            struct {
                lcb_http_status_t status;
                const char *path;
                lcb_size_t npath;
                const char *const *headers;
                const void *bytes;
                lcb_size_t nbytes;
            } v0;
        } v;
    } lcb_http_resp_t;
    typedef struct lcb_server_stat_resp_st {
        int version;
        union {
            struct {
                const char *server_endpoint;
                const void *key;
                lcb_size_t nkey;
                const void *bytes;
                lcb_size_t nbytes;
            } v0;
        } v;
    } lcb_server_stat_resp_t;
    typedef struct lcb_server_version_resp_st {
        int version;
        union {
            struct {
                const char *server_endpoint;
                const char *vstring;
                lcb_size_t nvstring;
            } v0;
        } v;
    } lcb_server_version_resp_t;
    typedef struct lcb_verbosity_resp_st {
        int version;
        union {
            struct {
                const char *server_endpoint;
            } v0;
        } v;
    } lcb_verbosity_resp_t;
    typedef struct lcb_flush_resp_st {
        int version;
        union {
            struct {
                const char *server_endpoint;
            } v0;
        } v;
    } lcb_flush_resp_t;
    lcb_error_t lcb_verify_struct_size(lcb_uint32_t id, lcb_uint32_t version,
                                       lcb_size_t size);
    enum lcb_compat_t {
LCB_MEMCACHED_CLUSTER=0,
LCB_CACHED_CONFIG=1,
    };
    typedef enum lcb_compat_t lcb_compat_t;
    typedef enum lcb_compat_t lcb_cluster_t;
    lcb_error_t lcb__create_compat_230(lcb_compat_t type,
                                       const void *specific,
                                       lcb_t *instance,
                                       struct lcb_io_opt_st *io);
    struct lcb_memcached_st {
        const char *serverlist;
        const char *username;
        const char *password;
    };
    struct lcb_cached_config_st {
        const char *cachefile;
        struct lcb_create_st createopt;
    };
    void lcb_behavior_set_syncmode(lcb_t instance, lcb_syncmode_t syncmode);
    lcb_syncmode_t lcb_behavior_get_syncmode(lcb_t instance);
    void lcb_behavior_set_ipv6(lcb_t instance, lcb_ipv6_t mode);
    lcb_ipv6_t lcb_behavior_get_ipv6(lcb_t instance);
    void lcb_behavior_set_config_errors_threshold(lcb_t instance, lcb_size_t num_events);
    lcb_size_t lcb_behavior_get_config_errors_threshold(lcb_t instance);
    typedef struct lcb_durability_cmd_st {
        int version;
        union {
            struct {
                const void *key;
                size_t nkey;
                const void *hashkey;
                size_t nhashkey;
                lcb_cas_t cas;
            } v0;
        } v;
    } lcb_durability_cmd_t;
    typedef struct lcb_durability_resp_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                lcb_error_t err;
                lcb_cas_t cas;
                unsigned char persisted_master;
                unsigned char exists_master;
                unsigned char npersisted;
                unsigned char nreplicated;
                unsigned short nresponses;
            } v0;
        } v;
    } lcb_durability_resp_t;
    typedef struct lcb_durability_opts_st {
        int version;
        union {
            struct {
                lcb_uint32_t timeout;
                lcb_uint32_t interval;
                lcb_uint16_t persist_to;
                lcb_uint16_t replicate_to;
                lcb_uint8_t check_delete;
                lcb_uint8_t cap_max;
            } v0;
        } v;
    } lcb_durability_opts_t;
    typedef void (*lcb_get_callback)(lcb_t instance,
                                     const void *cookie,
                                     lcb_error_t error,
                                     const lcb_get_resp_t *resp);
    typedef void (*lcb_store_callback)(lcb_t instance,
                                       const void *cookie,
                                       lcb_storage_t operation,
                                       lcb_error_t error,
                                       const lcb_store_resp_t *resp);
    typedef void (*lcb_remove_callback)(lcb_t instance,
                                        const void *cookie,
                                        lcb_error_t error,
                                        const lcb_remove_resp_t *resp);
    typedef void (*lcb_touch_callback)(lcb_t instance,
                                       const void *cookie,
                                       lcb_error_t error,
                                       const lcb_touch_resp_t *resp);
    typedef void (*lcb_unlock_callback)(lcb_t instance,
                                        const void *cookie,
                                        lcb_error_t error,
                                        const lcb_unlock_resp_t *resp);
    typedef void (*lcb_arithmetic_callback)(lcb_t instance,
                                            const void *cookie,
                                            lcb_error_t error,
                                            const lcb_arithmetic_resp_t *resp);
    typedef void (*lcb_observe_callback)(lcb_t instance,
                                         const void *cookie,
                                         lcb_error_t error,
                                         const lcb_observe_resp_t *resp);
    typedef void (*lcb_stat_callback)(lcb_t instance,
                                      const void *cookie,
                                      lcb_error_t error,
                                      const lcb_server_stat_resp_t *resp);
    typedef void (*lcb_version_callback)(lcb_t instance,
                                         const void *cookie,
                                         lcb_error_t error,
                                         const lcb_server_version_resp_t *resp);
    typedef void (*lcb_error_callback)(lcb_t instance,
                                       lcb_error_t error,
                                       const char *errinfo);
    typedef void (*lcb_flush_callback)(lcb_t instance,
                                       const void *cookie,
                                       lcb_error_t error,
                                       const lcb_flush_resp_t *resp);
    typedef void (*lcb_timer_callback)(lcb_timer_t timer,
                                       lcb_t instance,
                                       const void *cookie);
    typedef void (*lcb_http_complete_callback)(lcb_http_request_t request,
                                               lcb_t instance,
                                               const void *cookie,
                                               lcb_error_t error,
                                               const lcb_http_resp_t *resp);
    typedef void (*lcb_http_data_callback)(lcb_http_request_t request,
                                           lcb_t instance,
                                           const void *cookie,
                                           lcb_error_t error,
                                           const lcb_http_resp_t *resp);
    typedef void (*lcb_configuration_callback)(lcb_t instance,
                                               lcb_configuration_t config);
    typedef void (*lcb_verbosity_callback)(lcb_t instance,
                                           const void *cookie,
                                           lcb_error_t error,
                                           const lcb_verbosity_resp_t *resp);
    typedef void (*lcb_durability_callback)(lcb_t instance,
                                            const void *cookie,
                                            lcb_error_t err,
                                            const lcb_durability_resp_t *res);
    typedef void (*lcb_exists_callback)(lcb_t instance,
                                        const void *cookie,
                                        lcb_error_t err,
                                        const lcb_observe_resp_t *resp);
    typedef lcb_error_t (*lcb_errmap_callback)(lcb_t instance, lcb_uint16_t bincode);
    lcb_get_callback lcb_set_get_callback(lcb_t, lcb_get_callback);
    lcb_store_callback lcb_set_store_callback(lcb_t, lcb_store_callback);
    lcb_arithmetic_callback lcb_set_arithmetic_callback(lcb_t,
                                                        lcb_arithmetic_callback);
    lcb_observe_callback lcb_set_observe_callback(lcb_t, lcb_observe_callback);
    lcb_remove_callback lcb_set_remove_callback(lcb_t, lcb_remove_callback);
    lcb_stat_callback lcb_set_stat_callback(lcb_t, lcb_stat_callback);
    lcb_version_callback lcb_set_version_callback(lcb_t, lcb_version_callback);
    lcb_touch_callback lcb_set_touch_callback(lcb_t, lcb_touch_callback);
    lcb_error_callback lcb_set_error_callback(lcb_t, lcb_error_callback);
    lcb_flush_callback lcb_set_flush_callback(lcb_t, lcb_flush_callback);
    lcb_http_complete_callback lcb_set_http_complete_callback(lcb_t,
                                                              lcb_http_complete_callback);
    lcb_http_data_callback lcb_set_http_data_callback(lcb_t,
                                                      lcb_http_data_callback);
    lcb_unlock_callback lcb_set_unlock_callback(lcb_t, lcb_unlock_callback);
    lcb_configuration_callback lcb_set_configuration_callback(lcb_t,
                                                              lcb_configuration_callback);
    lcb_verbosity_callback lcb_set_verbosity_callback(lcb_t,
                                                      lcb_verbosity_callback);
    lcb_durability_callback lcb_set_durability_callback(lcb_t,
                                                        lcb_durability_callback);
    lcb_errmap_callback lcb_set_errmap_callback(lcb_t, lcb_errmap_callback);
struct event_base;
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
                                         lcb_uint32_t min,
                                         lcb_uint32_t max,
                                         lcb_uint32_t total,
                                         lcb_uint32_t maxtotal);
    lcb_error_t lcb_get_timings(lcb_t instance,
                                const void *cookie,
                                lcb_timings_callback callback);
    typedef struct lcb_cntl_vbinfo_st lcb_cntl_vbinfo_t;
    struct lcb_cntl_vbinfo_st {
        int version;
        union {
            struct {
                const void *key;
                lcb_size_t nkey;
                int vbucket;
                int server_index;
            } v0;
        } v;
    };
    typedef struct lcb_cntl_server_st lcb_cntl_server_t;
    struct lcb_cntl_server_st {
        int version;
        union {
            struct {
                int index; const char *host; const char *port; int connected; union { lcb_socket_t sockfd; lcb_sockdata_t *sockptr; } sock;
            } v0;
            struct {
                int index; const char *host; const char *port; int connected; union { lcb_socket_t sockfd; lcb_sockdata_t *sockptr; } sock;
                char *sasl_mech;
            } v1;
        } v;
    };
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
    const char *lcb_get_version(lcb_uint32_t *version);
    lcb_error_t lcb_create_io_ops(lcb_io_opt_t *op,
                                  const struct lcb_create_io_ops_st *options);
    lcb_error_t lcb_destroy_io_ops(lcb_io_opt_t op);
    lcb_error_t lcb_create(lcb_t *instance,
                           const struct lcb_create_st *options);
    void lcb_destroy(lcb_t instance);
    void lcb_set_timeout(lcb_t instance, lcb_uint32_t usec);
    lcb_uint32_t lcb_get_timeout(lcb_t instance);
    void lcb_set_view_timeout(lcb_t instance, lcb_uint32_t usec);
    lcb_uint32_t lcb_get_view_timeout(lcb_t instance);
    const char *lcb_get_host(lcb_t instance);
    const char *lcb_get_port(lcb_t instance);
    lcb_error_t lcb_connect(lcb_t instance);
    lcb_error_t lcb_get_last_error(lcb_t instance);
    const char *lcb_strerror(lcb_t instance, lcb_error_t error);
    void lcb_flush_buffers(lcb_t instance, const void *cookie);
    void lcb_set_cookie(lcb_t instance, const void *cookie);
    const void *lcb_get_cookie(lcb_t instance);
    lcb_error_t lcb_wait(lcb_t instance);
    int lcb_is_waiting(lcb_t instance);
    void lcb_breakout(lcb_t instance);
    lcb_error_t lcb_get(lcb_t instance,
                        const void *command_cookie,
                        lcb_size_t num,
                        const lcb_get_cmd_t *const *commands);
    lcb_error_t lcb_get_replica(lcb_t instance,
                                const void *command_cookie,
                                lcb_size_t num,
                                const lcb_get_replica_cmd_t *const *commands);
    lcb_error_t lcb_unlock(lcb_t instance,
                           const void *command_cookie,
                           lcb_size_t num,
                           const lcb_unlock_cmd_t *const *commands);
    lcb_error_t lcb_touch(lcb_t instance,
                          const void *command_cookie,
                          lcb_size_t num,
                          const lcb_touch_cmd_t *const *commands);
    lcb_error_t lcb_store(lcb_t instance,
                          const void *command_cookie,
                          lcb_size_t num,
                          const lcb_store_cmd_t *const *commands);
    lcb_error_t lcb_arithmetic(lcb_t instance,
                               const void *command_cookie,
                               lcb_size_t num,
                               const lcb_arithmetic_cmd_t *const *commands);
    lcb_error_t lcb_observe(lcb_t instance,
                            const void *command_cookie,
                            lcb_size_t num,
                            const lcb_observe_cmd_t *const *commands);
    lcb_error_t lcb_remove(lcb_t instance,
                           const void *command_cookie,
                           lcb_size_t num,
                           const lcb_remove_cmd_t *const *commands);
    lcb_error_t lcb_server_stats(lcb_t instance,
                                 const void *command_cookie,
                                 lcb_size_t num,
                                 const lcb_server_stats_cmd_t *const *commands);
    lcb_error_t lcb_server_versions(lcb_t instance,
                                    const void *command_cookie,
                                    lcb_size_t num,
                                    const lcb_server_version_cmd_t *const *commands);
    lcb_error_t lcb_set_verbosity(lcb_t instance,
                                  const void *command_cookie,
                                  lcb_size_t num,
                                  const lcb_verbosity_cmd_t *const *commands);
    lcb_error_t lcb_flush(lcb_t instance, const void *cookie,
                          lcb_size_t num,
                          const lcb_flush_cmd_t *const *commands);
    lcb_error_t lcb_make_http_request(lcb_t instance,
                                      const void *command_cookie,
                                      lcb_http_type_t type,
                                      const lcb_http_cmd_t *cmd,
                                      lcb_http_request_t *request);
    void lcb_cancel_http_request(lcb_t instance,
                                 lcb_http_request_t request);
    lcb_timer_t lcb_timer_create(lcb_t instance,
                                 const void *command_cookie,
                                 lcb_uint32_t usec,
                                 int periodic,
                                 lcb_timer_callback callback,
                                 lcb_error_t *error);
    lcb_error_t lcb_timer_destroy(lcb_t instance, lcb_timer_t timer);
    lcb_int32_t lcb_get_num_replicas(lcb_t instance);
    lcb_int32_t lcb_get_num_nodes(lcb_t instance);
    const char *const *lcb_get_server_list(lcb_t instance);
    lcb_error_t lcb_cntl(lcb_t instance, int mode, int cmd, void *arg);
    lcb_error_t lcb_durability_poll(lcb_t instance,
                                    const void *cookie,
                                    const lcb_durability_opts_t *options,
                                    lcb_size_t ncmds,
                                    const lcb_durability_cmd_t *const *cmds);
    lcb_error_t lcb_errmap_default(lcb_t instance, lcb_uint16_t code);
    void *lcb_mem_alloc(lcb_size_t size);
    void lcb_mem_free(void *ptr);
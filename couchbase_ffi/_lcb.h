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
typedef long lcb_time_t;
typedef char va_list;
    typedef enum {
        LCB_ERRTYPE_INPUT = 0x01,
        LCB_ERRTYPE_NETWORK = 0x02,
        LCB_ERRTYPE_FATAL = 0x04,
        LCB_ERRTYPE_TRANSIENT = 0x08,
        LCB_ERRTYPE_DATAOP = 0x10,
        LCB_ERRTYPE_INTERNAL = 0x20,
        LCB_ERRTYPE_PLUGIN = 0x40
    } lcb_errflags_t;
    typedef enum {
        LCB_SUCCESS = 0x00, LCB_AUTH_CONTINUE = 0x01, LCB_AUTH_ERROR = 0x02, LCB_DELTA_BADVAL = 0x03, LCB_E2BIG = 0x04, LCB_EBUSY = 0x05, LCB_EINTERNAL = 0x06, LCB_EINVAL = 0x07, LCB_ENOMEM = 0x08, LCB_ERANGE = 0x09, LCB_ERROR = 0x0A, LCB_ETMPFAIL = 0x0B, LCB_KEY_EEXISTS = 0x0C, LCB_KEY_ENOENT = 0x0D, LCB_DLOPEN_FAILED = 0x0E, LCB_DLSYM_FAILED = 0x0F, LCB_NETWORK_ERROR = 0x10, LCB_NOT_MY_VBUCKET = 0x11, LCB_NOT_STORED = 0x12, LCB_NOT_SUPPORTED = 0x13, LCB_UNKNOWN_COMMAND = 0x14, LCB_UNKNOWN_HOST = 0x15, LCB_PROTOCOL_ERROR = 0x16, LCB_ETIMEDOUT = 0x17, LCB_CONNECT_ERROR = 0x18, LCB_BUCKET_ENOENT = 0x19, LCB_CLIENT_ENOMEM = 0x1A, LCB_CLIENT_ETMPFAIL = 0x1B, LCB_EBADHANDLE = 0x1C, LCB_SERVER_BUG = 0x1D, LCB_PLUGIN_VERSION_MISMATCH = 0x1E, LCB_INVALID_HOST_FORMAT = 0x1F, LCB_INVALID_CHAR = 0x20, LCB_DURABILITY_ETOOMANY = 0x21, LCB_DUPLICATE_COMMANDS = 0x22, LCB_NO_MATCHING_SERVER = 0x23, LCB_BAD_ENVIRONMENT = 0x24, LCB_BUSY = 0x25, LCB_INVALID_USERNAME = 0x26, LCB_CONFIG_CACHE_INVALID = 0x27, LCB_SASLMECH_UNAVAILABLE = 0x28, LCB_TOO_MANY_REDIRECTS = 0x29,
        LCB_MAX_ERROR = 0x1000
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
        LCB_CONFIGURATION_NEW = 0x00,
        LCB_CONFIGURATION_CHANGED = 0x01,
        LCB_CONFIGURATION_UNCHANGED = 0x02
    } lcb_configuration_t;
    typedef enum {
        LCB_ADD = 0x01,
        LCB_REPLACE = 0x02,
        LCB_SET = 0x03,
        LCB_APPEND = 0x04,
        LCB_PREPEND = 0x05
    } lcb_storage_t;
    typedef enum {
        LCB_OBSERVE_FOUND = 0x00,
        LCB_OBSERVE_PERSISTED = 0x01,
        LCB_OBSERVE_NOT_FOUND = 0x80,
        LCB_OBSERVE_LOGICALLY_DELETED = 0x81,
        LCB_OBSERVE_MAX = 0x82
    } lcb_observe_t;
    typedef enum {
        LCB_TYPE_BUCKET = 0x00,
        LCB_TYPE_CLUSTER = 0x01
    } lcb_type_t;
    typedef int lcb_socket_t;
    typedef enum {
        LCB_IO_OPS_INVALID = 0x00,
        LCB_IO_OPS_DEFAULT = 0x01,
        LCB_IO_OPS_LIBEVENT = 0x02,
        LCB_IO_OPS_WINSOCK = 0x03,
        LCB_IO_OPS_LIBEV = 0x04,
        LCB_IO_OPS_SELECT = 0x05,
        LCB_IO_OPS_WINIOCP = 0x06,
        LCB_IO_OPS_LIBUV = 0x07
    } lcb_io_ops_type_t;
    typedef enum {
        LCB_VBUCKET_STATE_ACTIVE = 1,
        LCB_VBUCKET_STATE_REPLICA = 2,
        LCB_VBUCKET_STATE_PENDING = 3,
        LCB_VBUCKET_STATE_DEAD = 4
    } lcb_vbucket_state_t;
    typedef enum {
        LCB_VERBOSITY_DETAIL = 0x00,
        LCB_VERBOSITY_DEBUG = 0x01,
        LCB_VERBOSITY_INFO = 0x02,
        LCB_VERBOSITY_WARNING = 0x03
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
        LCB_ASYNCHRONOUS = 0x00,
        LCB_SYNCHRONOUS = 0xff
    } lcb_syncmode_t;
    typedef enum {
        LCB_IPV6_DISABLED = 0x00,
        LCB_IPV6_ONLY = 0x1,
        LCB_IPV6_ALLOW = 0x02
    } lcb_ipv6_t;
    typedef enum {
        LCB_LOG_TRACE = 0,
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
        LCB_CONFIG_TRANSPORT_LIST_END = 0,
        LCB_CONFIG_TRANSPORT_HTTP = 1,
        LCB_CONFIG_TRANSPORT_CCCP
    } lcb_config_transport_t;
    typedef enum {
        LCB_HTTP_TYPE_VIEW = 0,
        LCB_HTTP_TYPE_MANAGEMENT = 1,
        LCB_HTTP_TYPE_RAW = 2,
        LCB_HTTP_TYPE_MAX = 3
    } lcb_http_type_t;
    typedef enum {
        LCB_HTTP_METHOD_GET = 0,
        LCB_HTTP_METHOD_POST = 1,
        LCB_HTTP_METHOD_PUT = 2,
        LCB_HTTP_METHOD_DELETE = 3,
        LCB_HTTP_METHOD_MAX = 4
    } lcb_http_method_t;
    typedef enum {
        LCB_HTTP_STATUS_CONTINUE = 100,
        LCB_HTTP_STATUS_SWITCHING_PROTOCOLS = 101,
        LCB_HTTP_STATUS_PROCESSING = 102,
        LCB_HTTP_STATUS_OK = 200,
        LCB_HTTP_STATUS_CREATED = 201,
        LCB_HTTP_STATUS_ACCEPTED = 202,
        LCB_HTTP_STATUS_NON_AUTHORITATIVE_INFORMATION = 203,
        LCB_HTTP_STATUS_NO_CONTENT = 204,
        LCB_HTTP_STATUS_RESET_CONTENT = 205,
        LCB_HTTP_STATUS_PARTIAL_CONTENT = 206,
        LCB_HTTP_STATUS_MULTI_STATUS = 207,
        LCB_HTTP_STATUS_MULTIPLE_CHOICES = 300,
        LCB_HTTP_STATUS_MOVED_PERMANENTLY = 301,
        LCB_HTTP_STATUS_FOUND = 302,
        LCB_HTTP_STATUS_SEE_OTHER = 303,
        LCB_HTTP_STATUS_NOT_MODIFIED = 304,
        LCB_HTTP_STATUS_USE_PROXY = 305,
        LCB_HTTP_STATUS_UNUSED = 306,
        LCB_HTTP_STATUS_TEMPORARY_REDIRECT = 307,
        LCB_HTTP_STATUS_BAD_REQUEST = 400,
        LCB_HTTP_STATUS_UNAUTHORIZED = 401,
        LCB_HTTP_STATUS_PAYMENT_REQUIRED = 402,
        LCB_HTTP_STATUS_FORBIDDEN = 403,
        LCB_HTTP_STATUS_NOT_FOUND = 404,
        LCB_HTTP_STATUS_METHOD_NOT_ALLOWED = 405,
        LCB_HTTP_STATUS_NOT_ACCEPTABLE = 406,
        LCB_HTTP_STATUS_PROXY_AUTHENTICATION_REQUIRED = 407,
        LCB_HTTP_STATUS_REQUEST_TIMEOUT = 408,
        LCB_HTTP_STATUS_CONFLICT = 409,
        LCB_HTTP_STATUS_GONE = 410,
        LCB_HTTP_STATUS_LENGTH_REQUIRED = 411,
        LCB_HTTP_STATUS_PRECONDITION_FAILED = 412,
        LCB_HTTP_STATUS_REQUEST_ENTITY_TOO_LARGE = 413,
        LCB_HTTP_STATUS_REQUEST_URI_TOO_LONG = 414,
        LCB_HTTP_STATUS_UNSUPPORTED_MEDIA_TYPE = 415,
        LCB_HTTP_STATUS_REQUESTED_RANGE_NOT_SATISFIABLE = 416,
        LCB_HTTP_STATUS_EXPECTATION_FAILED = 417,
        LCB_HTTP_STATUS_UNPROCESSABLE_ENTITY = 422,
        LCB_HTTP_STATUS_LOCKED = 423,
        LCB_HTTP_STATUS_FAILED_DEPENDENCY = 424,
        LCB_HTTP_STATUS_INTERNAL_SERVER_ERROR = 500,
        LCB_HTTP_STATUS_NOT_IMPLEMENTED = 501,
        LCB_HTTP_STATUS_BAD_GATEWAY = 502,
        LCB_HTTP_STATUS_SERVICE_UNAVAILABLE = 503,
        LCB_HTTP_STATUS_GATEWAY_TIMEOUT = 504,
        LCB_HTTP_STATUS_HTTP_VERSION_NOT_SUPPORTED = 505,
        LCB_HTTP_STATUS_INSUFFICIENT_STORAGE = 507
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
        LCB_REPLICA_FIRST = 0x00,
        LCB_REPLICA_ALL = 0x01,
        LCB_REPLICA_SELECT = 0x02
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
        LCB_OBSERVE_MASTER_ONLY = 0x01
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
const char *
lcb_strerror(lcb_t, lcb_error_t);
lcb_error_t
lcb_create(lcb_t*, struct lcb_create_st *);
lcb_error_t
lcb_wait(lcb_t);
lcb_error_t
lcb_store(lcb_t, const void *, lcb_size_t, const lcb_store_cmd_t **);
lcb_error_t
lcb_get(lcb_t, const void *, lcb_size_t, const lcb_get_cmd_t **);
lcb_error_t
lcb_touch(lcb_t, const void *, lcb_size_t, const lcb_touch_cmd_t **);
lcb_error_t
lcb_remove(lcb_t, const void *, lcb_size_t, const lcb_remove_cmd_t **);
lcb_error_t
lcb_unlock(lcb_t, const void *, lcb_size_t, const lcb_unlock_cmd_t **);
lcb_error_t
lcb_arithmetic(lcb_t, const void *, lcb_size_t, const lcb_arithmetic_cmd_t **);
lcb_error_t
lcb_server_stats(lcb_t, const void *, lcb_size_t, const lcb_server_stats_cmd_t **);
lcb_error_t
lcb_observe(lcb_t, const void *, lcb_size_t, const lcb_observe_cmd_t **);
lcb_error_t
lcb_make_http_request(lcb_t, const void *, lcb_http_type_t,
                      const lcb_http_cmd_t *, lcb_http_request_t*);
lcb_error_t
lcb_durability_poll(lcb_t, const void *, const lcb_durability_opts_t *,
                    lcb_size_t, const lcb_durability_cmd_t **);
lcb_int32_t lcb_get_num_replicas(lcb_t);

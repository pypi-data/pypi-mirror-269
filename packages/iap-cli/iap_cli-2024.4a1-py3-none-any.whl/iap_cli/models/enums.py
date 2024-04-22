from enum import Enum


class Order(Enum):
    integer__1 = -1
    integer_1 = 1


class LogLevel(Enum):
    error = "error"
    warn = "warn"
    info = "info"
    debug = "debug"
    trace = "trace"
    spam = "spam"


class Method(Enum):
    get = "get"
    delete = "delete"
    patch = "patch"
    post = "post"
    put = "put"


class State(Enum):
    DEAD = "DEAD"
    DELETED = "DELETED"
    DISCONNECT = "DISCONNECT"
    RUNNING = "RUNNING"
    STARTING = "STARTING"
    STOPPED = "STOPPED"

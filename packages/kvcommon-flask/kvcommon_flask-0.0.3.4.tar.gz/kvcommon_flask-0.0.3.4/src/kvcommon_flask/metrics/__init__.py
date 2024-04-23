from prometheus_client import start_http_server

from kvcommon_flask.vars import KVC_FLASK_METRICS_ENABLED as ENABLED
from kvcommon_flask.vars import KVC_FLASK_METRICS_PORT
from .metrics import SCHEDULER_JOB_EVENT

from .metrics import APP_INFO
from .metrics import SERVER_REQUEST_SECONDS
from .metrics import incr
from .metrics import decr


def init_metrics():
    if ENABLED:
        start_http_server(KVC_FLASK_METRICS_PORT)

__all__ = [
    "ENABLED",
    "incr",
    "decr",
    "init_metrics",
    "SCHEDULER_JOB_EVENT",
    "APP_INFO",
    "SERVER_REQUEST_SECONDS",
]

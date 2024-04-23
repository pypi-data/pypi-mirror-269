import os
import typing as t

from kvcommon.types import to_bool

KVC_FLASK_METRICS_PORT = int(os.getenv("KVC_FLASK_METRICS_PORT", 9090))
KVC_FLASK_METRICS_ENABLED = to_bool(os.getenv("KVC_FLASK_METRICS_ENABLED", False))
KVC_FLASK_TRACES_ENABLED = to_bool(os.getenv("KVC_FLASK_TRACES_ENABLED", False))

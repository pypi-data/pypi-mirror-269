# KvCommon-Flask

Library of various [Flask](https://flask.palletsprojects.com/en/3.0.x/) utils that aren't worthy of their own dedicated libs.

This library isn't likely to be useful to anyone else; it's just a convenience to save me from copy/pasting between various projects I work on.

## Configuration & Env Vars

| Env Var | Default | Type | Description|
|---|---|---|---|
|`KVC_FLASK_METRICS_PORT`|`9090`|Int|Port on the server from which metrics can be scraped|
|`KVC_FLASK_METRICS_ENABLED`|`False`|Boolean|Toggles prometheus metrics|
|`KVC_FLASK_TRACES_ENABLED`|`False`|Boolean|Toggles OTLP traces|

## Packages/Modules

| Package | Description |
|---|---|
|`metrics`|Prometheus Metrics utils & boilerplate
|`traces`|OTLP Traces utils & boilerplate
|`context`|Convenience utils for manipulating Flask config and flask.g context
|`middleware`|Basic middleware class using flask-http-middleware with metrics
|`scheduler`|Utils for scheduling jobs on cron-like internvals with Flask-APScheduler and metrics + logging

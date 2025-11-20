from prometheus_client import Counter, Histogram
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, request
import time
from ..log import log

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["endpoint"])
ERROR_COUNT = Counter('errors_total', 'Total count of application errors', ["method", "endpoint", "error_type", "status_code"])

def setup_prometheus_metrics(app: Flask):
    @app.before_request
    def before_request():
        request._start_time = time.time()
        log.info("request_started") # , method=request.method, path=request.path, remote_addr=request.remote_addr)

    @app.after_request
    def after_request(response):
        latency = time.time() - getattr(request, "_start_time", time.time())
        endpoint = request.path
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
        log.info("request_finished") # , method=request.method, path=request.path, status=response.status_code, latency=latency)
        return response
    
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

    return app

from flask_limiter import Limiter
from flask import Flask
from ...utils.log import log
import os

if os.getenv("RATE_LIMIT_BY_X_FORWARDED_FOR", "0").lower() in ['true', '1', 'yes', 'enabled', 'on', 'enable']:
    from flask import request
    key_func = lambda: request.headers.get("X-Forwarded-For", request.remote_addr) or "127.0.0.1"
else:
    from flask_limiter.util import get_remote_address
    key_func = get_remote_address

limiter = Limiter(key_func=key_func, default_limits=["50/minute"])

def setup_rate_limiter(app: Flask):
    global limiter
    limiter.init_app(app)
    return app

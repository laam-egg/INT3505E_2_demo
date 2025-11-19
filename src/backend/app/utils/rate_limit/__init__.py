from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask

limiter = Limiter(key_func=get_remote_address, default_limits=["50/minute"])

def setup_rate_limiter(app: Flask):
    global limiter
    limiter.init_app(app)
    return app

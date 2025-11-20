import traceback
from flask import Flask, url_for, request, got_request_exception
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os
from werkzeug.exceptions import HTTPException

from .utils.prometheus_metrics import setup_prometheus_metrics, ERROR_COUNT
from .utils.rate_limit import setup_rate_limiter

from .utils.log import log

app = Flask(__name__)

def handle_every_exception(exception):
    status_code = 500
    if isinstance(exception, HTTPException):
        status_code = exception.code
    ERROR_COUNT.labels(method=request.method, endpoint=request.path, error_type=type(exception).__name__, status_code=status_code).inc()
    log.error(''.join(traceback.TracebackException.from_exception(exception).format()))
    return {"error": str(exception), "message": "Internal Server Error!!!"}, status_code

@app.errorhandler(Exception)
def handle_Exception(exception):
    return handle_every_exception(exception)

def handle_request_exception(sender, exception, *args, **kwargs):
    handle_every_exception(exception)
    return

got_request_exception.connect(handle_request_exception, app)


app = setup_prometheus_metrics(app)
app = setup_rate_limiter(app)

app.url_map.strict_slashes = False

CORS(app)  # Enable CORS for all routes

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
if not JWT_SECRET_KEY:
    raise RuntimeError(f"Environment variable JWT_SECRET_KEY not set")

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

with app.app_context():
    from .controllers import register_api_controllers
    register_api_controllers(app)

    @app.get('/')
    def home():
        return f"""
        <html><head><title>Library Management System - Backend</title></head><body>
        <h1>Welcome to the Library Management System backend server!</h1>
        <a href={url_for("get_api_versions")}>Here is the API documentation.</a>
        </body></html>
        """

print(app.url_map)

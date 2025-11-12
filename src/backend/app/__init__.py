from flask import Flask, url_for, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, url_for, jsonify, request
from flask_cors import CORS
import jwt
import os

from .services.AccessTokenService import AccessTokenService
from .services.UserService import UserService
from .services.AuthService import AuthService

app = Flask(__name__)

FRONTEND_BASE_URLS = os.getenv("FRONTEND_BASE_URLS", "")
if not FRONTEND_BASE_URLS:
    raise RuntimeError("Environment variable FRONTEND_BASE_URLS not set.")

CORS(app, origins=FRONTEND_BASE_URLS.split(','), supports_credentials=True)


with app.app_context():
    access_token_service = AccessTokenService()
    user_service = UserService(access_token_service)
    auth_service = AuthService(access_token_service)
    
    @app.get('/')
    def home():
        return f"""
        <html><head><title>Auth Demo</title></head><body>
        <h1>Auth Demo</h1>
        <div>
            <p>Demo 3 cách lưu access token vào:</p>
            <ol>
                <li>localStorage</li>
                <li>sessionStorage</li>
                <li>HTTP-Only Cookie</li>
            </ol>
        </div>
        </body></html>
        """
    

    @app.post('/by-header/auth/login')
    @auth_service.write_token(mode='Header')
    def byheader_login():
        req = request.get_json()
        return user_service.login(req)
    
    @app.get('/by-header/users')
    @auth_service.require_token('Header')
    def byheader_get_users(email):
        return user_service.get_users()
    


    @app.post('/by-cookie/auth/login')
    @auth_service.write_token(mode='Cookie')
    def bycookie_login():
        req = request.get_json()
        return user_service.login(req)
    
    @app.get('/by-cookie/users')
    @auth_service.require_token('Cookie')
    def bycookie_get_users(email):
        return user_service.get_users()



print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)

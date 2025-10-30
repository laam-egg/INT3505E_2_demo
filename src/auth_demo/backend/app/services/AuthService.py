from .AccessTokenService import AccessTokenService
from flask import request, make_response
from typing import Literal

AuthMode = Literal['Header', 'Cookie']

class AuthService:
    def __init__(self, access_token_service: AccessTokenService):
        self.access_token_service = access_token_service
        self.auth_cookie_name = 'auth'
    
    def require_token(self, mode: AuthMode):
        if mode == 'Header':
            def actual_decorator(func):
                def wrapper(*args, **kwargs):
                    authHeader = request.headers.get('Authorization', "")
                    if not authHeader:
                        return { "error": "Token not provided in Authorization header" }, 401
                    BEARER_PREFIX = "Bearer "
                    if not authHeader.startswith(BEARER_PREFIX):
                        return { "error": "Not a Bearer token" }, 401
                    token = authHeader[len(BEARER_PREFIX):]
                    if not token:
                        return { "error": "Token is empty" }, 401
                    
                    try:
                        email = self.access_token_service.verify(token)
                    except Exception as e:
                        return { "error": str(e) }, 401
                    
                    return func(*args, **kwargs, email=email)
                
                wrapper.__name__ = func.__name__
                return wrapper
        
        elif mode == 'Cookie':
            def actual_decorator(func):
                def wrapper(*args, **kwargs):
                    authCookie = request.cookies.get(self.auth_cookie_name, "")
                    if not authCookie:
                        return { "error": "Authentication cookie not submitted" }, 401
                    
                    try:
                        email = self.access_token_service.verify(authCookie)
                    except Exception as e:
                        return { "error": str(e) }, 401
                    
                    return func(*args, **kwargs, email=email)
                
                wrapper.__name__ = func.__name__
                return wrapper
        
        else:
            raise RuntimeError(f"No such mode: {mode}")
        
        return actual_decorator
    
    def write_token(self, mode: AuthMode):
        if mode == 'Cookie':
            def actual_decorator(func):
                def wrapper(*args, **kwargs):
                    res_body, status = func(*args, **kwargs)
                    token = res_body['token']
                    res = make_response(res_body)
                    res.set_cookie(
                        self.auth_cookie_name,
                        token,
                        max_age=11_520_000,
                        samesite='None',
                        secure=True,
                        httponly=True,
                    )
                    return res
                
                wrapper.__name__ = func.__name__
                return wrapper
            
        else:
            def actual_decorator(func):
                return func
        
        return actual_decorator

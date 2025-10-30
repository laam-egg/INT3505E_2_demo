import jwt
import os

class AccessTokenService:
    def __init__(self, secret_key: str = ""):
        if not secret_key:
            JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
            if not JWT_SECRET_KEY:
                raise RuntimeError(f"Environment variable JWT_SECRET_KEY not set")
            secret_key = JWT_SECRET_KEY
        self.secret_key = secret_key
        self.algorithm = 'HS256'

    def issue(self, email):
        return jwt.encode(
            {
                "sub": email,
                "iss": "AUTH_DEMO",
            },
            self.secret_key,
            self.algorithm,
        )
    
    def verify(self, token):
        try:
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            assert isinstance(decoded_payload, dict)
            assert 'sub' in decoded_payload
            email = decoded_payload['sub']
            assert isinstance(email, str)
            return email
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token.")
        except (AssertionError, KeyError) as e:
            raise Exception("Invalid token: " + str(e))

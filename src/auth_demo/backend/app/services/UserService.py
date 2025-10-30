from .AccessTokenService import AccessTokenService
from ordered_set import OrderedSet

class UserService:
    def __init__(self, access_token_service: AccessTokenService):
        self.access_token_service = access_token_service
        self.authenticated_emails = OrderedSet()

    def login(self, req):
        try:
            assert isinstance(req, dict)
            email = req['email']
            password = req['password']
            assert isinstance(email, str)
            assert isinstance(password, str)
        except (AssertionError, KeyError) as e:
            return { "error": str(e) }, 400
        
        if email.endswith("@legit.com") and password == email:
            self.authenticated_emails.add(email)
            token = self.access_token_service.issue(email)
            return { "token": token }, 200
        else:
            return { "error": "Wrong email or password" }, 401
    
    def get_users(self):
        return {
            "content": [
                *self.authenticated_emails,
            ],
        }, 200

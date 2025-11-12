from typing import Any
from ...utils.pageable import Pageable
from ..BaseCRUDService import BaseCRUDService
from flask_jwt_extended import create_access_token
from flask_restx import abort
import bcrypt
import base64
from typing import override

class UserService(BaseCRUDService):
    def __init__(self, collection=None) -> None:
        if collection is None:
            from ...db import users_collection
            collection = users_collection
        super().__init__(collection)
    
    def hash_password(self, password: str):
        password_hash = base64.b64encode(
            bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        ).decode('utf-8')
        return password_hash
    
    def check_password(self, password: str, password_hash: str):
        ph = base64.b64decode(
            password_hash.encode('utf-8')
        )
        matched = bcrypt.checkpw(password.encode('utf-8'), ph)
        return matched
    



    @override
    def post_item(self, item_doc):
        password = item_doc["password"]

        password_hash = self.hash_password(password)

        item_doc = {
            **item_doc,
            "password_hash": password_hash
        }

        return super().post_item(item_doc)
    
    @override
    def put_item_by_id(self, id, item_doc):
        raise NotImplementedError
    
    @override
    def patch_item_by_id(self, id, item_patch_doc):
        if "password_hash" in item_patch_doc:
            abort(400, "Payload không hợp lệ") # type: ignore
            raise RuntimeError
        
        if "password" in item_patch_doc:
            password = item_patch_doc["password"]
            password_hash = self.hash_password(password)
            item_patch_doc = {
                **item_patch_doc,
                "password_hash": password_hash,
            }
        
        return super().patch_item_by_id(id, item_patch_doc)
    
    def get_item_by_email(self, email):
        result = self.collection.find_one({ "email": email })
        if not result or result is None:
            abort(404, "Không có người dùng nào có email này.") # type: ignore
            raise RuntimeError
        return result
    
    def login(self, email, password):
        user = self.get_item_by_email(email)
        password_hash = user["password_hash"]
        matched = self.check_password(password, password_hash)
        if not matched:
            abort(401, "Sai mật khẩu") # type: ignore
            raise RuntimeError

        access_token = create_access_token(identity=email)
        return {
            "user": user,
            "accessToken": access_token
        }

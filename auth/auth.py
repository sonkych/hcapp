from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import config
import jwt


class Auth:
    def __init__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        self.credentials = credentials
        try:
            token = self.credentials.credentials
            payload = jwt.decode(token, config().app_key, algorithms=["HS256"])
            self.user_id = payload.get("user_id")
        except jwt.exceptions.DecodeError:
            self.user_id = None

    def authenticated(self):
        return self.user_id is not None

    def id(self):
        return self.user_id

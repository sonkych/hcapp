from passlib.context import CryptContext

from models.auth_token import AuthToken
from models.user import User
from datetime import datetime, timedelta
from config import config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from responses import *
import jwt
from database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
DB = next(get_db())


def user_to_dict(db_user):
    return {
        "company_id": db_user.company_id,
        "id": db_user.id,
        "email": db_user.email,
        "firstname": db_user.firstname,
        "lastname": db_user.lastname,
        "phone": db_user.phone,
        "telegram": db_user.telegram,
        "department": db_user.department,
        "position": db_user.position,
    }


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_bearer_token(user: User):
    data = {"user_id": user.id}
    expires_delta = timedelta(minutes=300)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, config().app_key)
    auth_token = AuthToken(
        user_id=user.id,
        token=token,
        expired_at=expire.strftime("%Y-%m-%d %H:%M:%S"),
    )

    DB.add(auth_token)
    DB.commit()
    return token


def revoke_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    db_token = DB.query(AuthToken).filter(AuthToken.token == token).first()
    if db_token:
        DB.delete(db_token)
        DB.commit()


def get_auth_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        db_token = DB.query(AuthToken).filter(AuthToken.token == token).first()
        if db_token is None or db_token.expired_at <= datetime.utcnow():
            return error_response("Invalid token", 401)

        payload = jwt.decode(token, config().app_key, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            return error_response("Unauthenticated", 401)
        return user_id
    except jwt.exceptions.DecodeError:
        return error_response("Invalid token", 401)

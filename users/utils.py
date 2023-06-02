from passlib.context import CryptContext
from models.user import User
from datetime import datetime, timedelta
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


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
        "hashed_password": db_user.hashed_password,
    }


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_bearer_token(user: User):
    data = {"sub": user.email}
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

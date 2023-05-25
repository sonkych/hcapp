from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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



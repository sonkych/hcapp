from auth.schemas import NewAccountForm
from database import get_db
from models.user import User as UserModel, Account, User
from users.schemas import UserCreate, UserUpdate
from users.utils import user_to_dict, get_password_hash, get_bearer_token, verify_password
from responses import error_response, success_response
from models.role import ROLE_USER, RoleModel

DB = next(get_db())


def get_account(account_id: int):
    return DB.query(UserModel).filter(Account.id == account_id).first()


def create_account(new_account: NewAccountForm, role=ROLE_USER):
    role_id = DB.query(RoleModel).filter(RoleModel.name == role).first()

    hashed_password = get_password_hash(new_account.password)

    db_company = Account(company_name=new_account.company_name)
    DB.add(db_company)
    DB.commit()

    db_user = UserModel(company_id=db_company.id,
                        email=new_account.email,
                        hashed_password=hashed_password,
                        firstname=new_account.firstname,
                        lastname=new_account.lastname,
                        phone=new_account.phone,
                        roles=[role_id])
    DB.add(db_user)
    DB.commit()
    DB.refresh(db_user)
    return success_response({"user": user_to_dict(db_user), "token": get_bearer_token(db_user)})


def get_user(user_id: int):
    db_user = DB.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        return user_to_dict(db_user)
    return error_response("User not found", 404)


def get_user_by_email(email: str):
    return DB.query(UserModel).filter(UserModel.email == email).first()


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return error_response("Incorrect email or password", 401)
    return success_response({"user": user_to_dict(user), "token": get_bearer_token(user)})


def get_users(auth_user, skip: int = 0, limit: int = 100) -> list[dict]:
    users = DB.query(UserModel).filter(UserModel.company_id == auth_user['company_id']).offset(skip).limit(limit).all()
    return list(map(user_to_dict, users))


def create_user(new_user: UserCreate):
    hashed_password = get_password_hash(new_user.password)
    new_user_dict = new_user.dict()
    del new_user_dict['password']  # Remove the password field
    print(new_user_dict)
    new_user_dict["hashed_password"] = hashed_password
    db_user = UserModel(**new_user_dict)

    # First version of this code:
    # db_user = UserModel(company_id=new_user.company_id,
    #                     email=new_user.email,
    #                     hashed_password=fake_hashed_password,
    #                     firstname=new_user.firstname,
    #                     lastname=new_user.lastname,
    #                     phone=new_user.phone,
    #                     telegram=new_user.telegram,
    #                     department=new_user.department,
    #                     position=new_user.position)

    DB.add(db_user)
    DB.commit()
    DB.refresh(db_user)
    return user_to_dict(db_user)


def update_user(user_id: int, updated_data: UserUpdate):
    user = DB.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        # Check if the updated email already exists for another user
        if updated_data.email != user.email and DB.query(UserModel).filter(
                UserModel.email == updated_data.email).first():
            return error_response("Email already registered", 400)

        # Update only the specified fields
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        DB.commit()
        DB.refresh(user)
        return user
    return None


def delete_user(user_id: int):
    db_user = DB.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        DB.delete(db_user)
        DB.commit()
        return True
    else:
        return False

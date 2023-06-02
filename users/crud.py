from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.schemas import NewAccountForm
from models.user import User as UserModel, Account
from responses import *
from users.schemas import UserCreate, UserUpdate
from users.utils import *


def get_account(db: Session, account_id: int):
    return db.query(UserModel).filter(Account.id == account_id).first()


def create_account(db: Session, new_account: NewAccountForm):
    hashed_password = get_password_hash(new_account.password)

    db_company = Account(company_name=new_account.company_name)
    db.add(db_company)
    db.commit()

    db_user = UserModel(company_id=db_company.id,
                        email=new_account.email,
                        hashed_password=hashed_password,
                        firstname=new_account.firstname,
                        lastname=new_account.lastname,
                        phone=new_account.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return success_response({"user": user_to_dict(db_user), "token": get_bearer_token(db_user)})


def get_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        return user_to_dict(db_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return error_response("Incorrect email or password", 401)
    return success_response({"user": user_to_dict(user), "token": get_bearer_token(user)})


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, new_user: UserCreate):
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

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user_to_dict(db_user)


def update_user(user_id: int, updated_data: UserUpdate, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        # Check if the updated email already exists for another user
        if updated_data.email != user.email and db.query(UserModel).filter(
                UserModel.email == updated_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Update only the specified fields
        for field, value in updated_data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user
    return None


def delete_user(user_id: int, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return False

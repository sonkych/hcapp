from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.schemas import LoginForm, NewAccountForm
from database import get_db
from responses import *
from users import crud

router = APIRouter()


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@router.post("/sign-in", response_model=AuthSuccessResponse)
def sign_in(login_form: LoginForm, db: Session = Depends(get_db)):
    return crud.authenticate_user(db, login_form.email, login_form.password)


@router.get("/sign-out")
def logout():
    return {"message": "Logged out successfully"}


@router.post("/recover")
def recover_password():
    return {"message": "Check Your you email for further details"}


@router.post("/sign-up", response_model=AuthSuccessResponse)
def create_account(register_form: NewAccountForm, db: Session = Depends(get_db)):
    db_account = crud.get_user_by_email(db, email=register_form.email)
    if db_account:
        return error_response("Email already registered", 400)
    return crud.create_account(db=db, new_account=register_form)

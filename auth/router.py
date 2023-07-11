from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.schemas import LoginForm, NewAccountForm
from models.role import ROLE_ADMIN
from responses import *
from users import crud
from users.utils import get_auth_user_id, revoke_bearer_token


router = APIRouter()
security = HTTPBearer()


@router.post("/sign-in", response_model=AuthSuccessResponse)
def sign_in(login_form: LoginForm):
    return crud.authenticate_user(login_form.email, login_form.password)


@router.post("/sign-out")
def logout(auth_user_id=Depends(get_auth_user_id), credentials: HTTPAuthorizationCredentials = Depends(security)):
    revoke_bearer_token(credentials)
    return {"message": "Logged out successfully"}


@router.post("/recover")
def recover_password():
    return {"message": "Check Your you email for further details"}


@router.post("/sign-up", response_model=AuthSuccessResponse)
def create_account(register_form: NewAccountForm):
    db_account = crud.get_user_by_email(email=register_form.email)
    if db_account:
        return error_response("Email already registered", 400)
    return crud.create_account(new_account=register_form, role=ROLE_ADMIN)

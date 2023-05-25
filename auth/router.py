from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from database import get_db
from auth.schemas import LoginForm, NewAccountForm
from users.schemas import User
from sqlalchemy.orm import Session
from database import SessionLocal
from users import crud

router = APIRouter()


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@router.post("/sign-in")
def sign_in(login_form: LoginForm, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, login_form.email, login_form.password)
    if db_user:
        return {"status": 200, "user": db_user}
    else:
        raise HTTPException(status_code=500, detail="Authentication Error")

    # Working code, first version without autenticate_user func
    # db_user = crud.get_user_by_email(db, email=login_form.email)
    # if db_user:
    #     if db_user.hashed_password == login_form.password + "notreallyhashed":
    #         return {"status": 200, "user": db_user}
    #     else:
    #         raise HTTPException(status_code=404, detail="Wrong Password")
    # else:
    #     raise HTTPException(status_code=404, detail="Wrong username")


@router.get("/sign-out")
def logout():
    return {"message": "Logged out successfully"}


@router.post("/recover")
def recover_password():
    return {"message": "Check Your you email for further details"}


@router.post("/sign-up", response_model=User)
def create_account(register_form: NewAccountForm, db: Session = Depends(get_db)):
    db_account = crud.get_user_by_email(db, email=register_form.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, new_account=register_form)






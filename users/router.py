from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError

from responses import *
from users import crud
from users.utils import get_auth_user_id
from users.schemas import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/users", response_model=GetUsersResponse)
def read_users(auth_user_id=Depends(get_auth_user_id)):
    if not isinstance(auth_user_id, int):
        return auth_user_id
    try:
        users = crud.get_users(crud.get_user(auth_user_id))
        return success_response(users)
    except ValidationError as e:
        print(e.errors())
        raise HTTPException(status_code=500, detail="Validation error occurred")


@router.post("/new-user", response_model=User)
def create_user(register_form: UserCreate):
    db_user = crud.get_user_by_email(email=register_form.email)
    db_account = crud.get_account(account_id=register_form.company_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not db_account:
        raise HTTPException(status_code=400, detail="Account not registered")

    return crud.create_user(new_user=register_form)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    return crud.get_user(user_id=user_id)


@router.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_data: UserUpdate):
    db_user = crud.update_user(user_id=user_id, updated_data=updated_data)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    deleted = crud.delete_user(user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "message": "User deleted"}

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from users.schemas import User, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from database import SessionLocal
from users import crud


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    try:
        users = crud.get_users(db=db)  # Fetch users from the database
        return users
    except ValidationError as e:
        print(e.errors())
        raise HTTPException(status_code=500, detail="Validation error occurred")


@router.post("/new-user", response_model=User)
def create_user(register_form: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=register_form.email)
    db_account = crud.get_account(db, account_id=register_form.company_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not db_account:
        raise HTTPException(status_code=400, detail="Account not registered")

    return crud.create_user(db=db, new_user=register_form)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)


@router.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, updated_data=updated_data)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(user_id=user_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "message": "User deleted"}

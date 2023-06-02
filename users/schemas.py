import re

from pydantic import BaseModel, EmailStr, validator, ValidationError, Field
from typing import Optional


class User(BaseModel):
    company_id: int
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    phone: str
    telegram: Optional[str]
    department: Optional[str]
    position: Optional[str]

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    company_id: int
    email: EmailStr
    firstname: str
    lastname: str
    phone: str = Field(..., max_length=15, regex=r'^\+\d{1,3}\d+$', description="+37256000000")  # Phone number pattern (e.g., +37256669625)
    telegram: str = Field(max_length=32)
    department: str
    position: str
    password: str = Field(...,
                          min_length=8,
                          max_length=15,
                          description="Password must contain at least one digit and one uppercase letter")

    @validator('password')
    def validate_password(cls, password):
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit and one uppercase letter')
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one digit and one uppercase letter')
        return password

    @validator('phone')
    def validate_phone(cls, phone):
        # Custom validation logic for the phone number
        # You can add additional checks or customize the validation as per your requirements
        if len(phone) < 5:
            raise ValidationError('Phone number is too short')
        return phone

    @validator('telegram')
    def validate_telegram(cls, telegram):
        # Custom validation logic for the Telegram username
        # You can add additional checks or customize the validation as per your requirements
        if telegram:
            if not re.match(r'^@\w{5,32}$', telegram):
                raise ValueError('Invalid telegram username format')
            elif len(telegram) < 6:
                raise ValidationError('Telegram username is too short')
        return telegram


class UserUpdate(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    phone: str = Field(..., min_length=6, max_length=15, description="+37256000000")  # Phone number pattern (e.g., +37256669625)
    telegram: str = Field(max_length=32)
    department: str
    position: str

    @validator('phone')
    def validate_phone(cls, phone):
        # Custom validation logic for the phone number
        # You can add additional checks or customize the validation as per your requirements
        if not re.match(r'^\+\d{1,3}\d+$', phone):
            raise ValueError('Invalid phone format')
        return phone

    @validator('telegram')
    def validate_telegram(cls, telegram):
        # Custom validation logic for the Telegram username
        # You can add additional checks or customize the validation as per your requirements
        if telegram:
            if not re.match(r'^@\w{5,32}$', telegram):
                raise ValueError('Invalid telegram username format')
            elif len(telegram) < 6:
                raise ValidationError('Telegram username is too short')
        return telegram


class UserPasswordUpdate(BaseModel):
    password: str = Field(..., min_length=8, max_length=15,
                          description="Password must contain at least one digit and one uppercase letter")

    @validator('password')
    def validate_password(cls, password):
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit and one uppercase letter')
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one digit and one uppercase letter')
        return password

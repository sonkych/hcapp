from pydantic import BaseModel, EmailStr, validator, ValidationError, Field


class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(...)

    # @validator('password')
    # def validate_password(cls, password):
    #     if not any(char.isdigit() for char in password):
    #         raise ValueError('Wrong password by validator')
    #     if not any(char.isupper() for char in password):
    #         raise ValueError('Wrong password by validator')
    #     if len(password) < 8:
    #         raise ValueError('Wrong password by validator')
    #     if len(password) > 15:
    #         raise ValueError('Wrong password by validator')
    #     return password


class NewAccountForm(BaseModel):
    company_name: str = Field(max_length=30)
    firstname: str = Field(max_length=30)
    lastname: str = Field(max_length=30)
    email: EmailStr
    phone: str = Field(..., max_length=15, regex=r'^\+\d{1,3}\d+$', description="+37256000000")
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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



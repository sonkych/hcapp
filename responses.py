from pydantic import BaseModel
from fastapi.responses import JSONResponse


def success_response(data):
    return {
        'success': True,
        'error_message': None,
        'data': data,
    }


def error_response(error_message, status=400, data=None):
    detail = {
        'success': False,
        'error_message': error_message,
        'data': data,
    }
    return JSONResponse(content=detail, status_code=status)


class Response(BaseModel):
    success: bool
    error_message: str | None


class UserResponse(BaseModel):
    company_id: int
    id: int
    email: str
    firstname: str
    lastname: str
    phone: str
    telegram: str | None
    department: str | None
    position: str | None


class UserWithTokenResponse(BaseModel):
    user: UserResponse
    token: str


class AuthSuccessResponse(Response):
    data: UserWithTokenResponse

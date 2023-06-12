from sqlalchemy import Column, Boolean, Integer, ForeignKey, String, TIMESTAMP
from models.model import BaseModel


class AuthToken(BaseModel):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String)
    expired_at = Column(TIMESTAMP)

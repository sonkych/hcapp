from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.model import BaseModel

user_role = Table('role_user',
                  BaseModel.metadata,
                  Column('role_id', Integer, ForeignKey('roles.id')),
                  Column('user_id', Integer, ForeignKey('users.id')),
                  )

ROLE_ADMIN = 'admin'
ROLE_USER = 'user'
ROLE_SUPER_ADMIN = 'super-admin'


class RoleModel(BaseModel):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('User', secondary=user_role, back_populates='roles')

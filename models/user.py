from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    company_name = Column(String)
    is_active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "user"
    company_id = Column(Integer, ForeignKey("company.id"))
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    email = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)
    telegram = Column(String)
    department = Column(String)
    position = Column(String)
    hashed_password = Column(String)



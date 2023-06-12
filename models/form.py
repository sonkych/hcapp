from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, JSON
from models.model import BaseModel


class Form(BaseModel):
    __tablename__ = "form"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    form_name = Column(String)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON)
    access = Column(JSON)
    routes = Column(JSON)
    fields = Column(JSON)
    extensions = Column(JSON)


class FormField(BaseModel):
    __tablename__ = "formfield"

    form_id = Column(Integer, ForeignKey("form.id"))
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    in_title = Column(Boolean)
    visible_on_step = Column(Integer)
    required_on_step = Column(Integer)
    immutable_from_step = Column(Integer)
    show_if = Column(JSON)
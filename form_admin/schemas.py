from pydantic import BaseModel, EmailStr, Json, StrictBool
from typing import Optional, Union, Dict, List


class Extension(BaseModel):
    id: int
    name: str
    data: dict
    is_active: bool


class FormSettings(BaseModel):
    name: str
    icon: str
    icon_color: str
    folder: str
    template: Union[str, bool] = False
    print_templates: list[Dict]


class FormAccess(BaseModel):
    permissions: list[Dict]


class Step(BaseModel):
    step_id: int
    step_name: str
    responsible: list


class Route(BaseModel):
    steps: list[Step]
    pass


class RoutesRead(BaseModel):
    users: list[Dict]
    steps: list[Step]


class FieldType(BaseModel):
    pass


class SystemFieldType(BaseModel):
    pass


class CreateForm(BaseModel):
    company_id: int
    name: str
    folder: dict
    settings: dict
    template: dict
    access: list
    routes: list
    fields: list


# Form Field Scheme
class FormField(BaseModel):
    id: int
    name: str
    type: str
    in_title: bool
    visible_on_step: int
    required_on_step: int
    immutable_from_step: int
    show_if: dict


class SystemField(BaseModel):
    id: int
    type: SystemFieldType
    in_title: bool
    visible_on_step: int


class FormTemplate(BaseModel):
    fields: list[FormField, SystemField]


class Form(BaseModel):
    company_id: int
    form_id: int
    settings: FormSettings
    access: list  # [list[user_id]
    routes: list
    fields: list[FormField]
    extensions: list[Extension]


# FIELD TYPES
class Text(FieldType):
    type: str = "text"
    name: str
    value: str
    width: int  # возможность настраивать ширину поля
    max_char: int
    default_value: str


class TextArea(FieldType):
    name: str
    value: str
    max_char: int
    default_value: str


class Number(FieldType):
    name: str
    value: str
    max_char: int
    default_value: str
    decimals: float
    money: bool
    currency: Json
    calculated: dict


class Checkmark(FieldType):
    name: str
    value: bool
    default_value: bool


class Date(FieldType):
    name: str
    format: Json
    default_value: str


class DueDate(FieldType):
    name: str
    format: Json
    default_value_days: int
    default_value_condition: Json


class FormTemplateCreate(BaseModel):
    fields: list[FieldType]

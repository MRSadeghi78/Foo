from pydantic import EmailStr
from sqlmodel import SQLModel

from database.models import UIDModelBase


class UserCreateSchema(UIDModelBase):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool


class UserInSchema(SQLModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

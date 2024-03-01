from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseSchema):
    name: str
    email: str
    role: Enum
    is_active: bool


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseSchema):
    user_id: int
    token: str
    expiry: datetime


class RestaurantSchema(BaseModel):
    name: str
    email: str
    mobile: str
    address: str
    opening_time: str
    closing_time: str
    logo: UploadFile


class CreateItemSchema(BaseModel):
    restaurant_id: int
    name: str
    description: str
    cost: float
    price: float
    is_active: bool
    image: UploadFile


class UpdateItemSchema(BaseModel):
    name: str
    description: str
    cost: float
    price: float
    is_active: bool
    image: UploadFile

from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """
        Base schema representing common fields for data models.

        This class defines attributes for common fields such as id, created_at, and updated_at.

        :ivar id: Unique identifier for the data model.
        :ivar created_at: Date and time when the record was created.
        :ivar updated_at: Date and time when the record was last updated.
    """
    id: int
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseSchema):
    """
        Schema representing user data.

        Inherits from BaseSchema.

        :ivar name: Name of the user.
        :ivar email: Email address of the user.
        :ivar role: Role of the user.
        :ivar is_active: Boolean indicating whether the user is active.
    """
    name: str
    email: str
    role: Enum
    is_active: bool


class LoginSchema(BaseModel):
    """
        Schema representing login credentials.

        :ivar email: Email address of the user.
        :ivar password: Password of the user.
    """
    email: str
    password: str


class TokenSchema(BaseSchema):
    """
        Schema representing authentication token data.

        Inherits from BaseSchema.

        :ivar user_id: ID of the associated user.
        :ivar token: Authentication token.
        :ivar expiry: Expiry date of the token.
    """
    user_id: int
    token: str
    expiry: datetime


class RestaurantSchema(BaseModel):
    """
        Schema representing restaurant data.

        :ivar name: Name of the restaurant.
        :ivar email: Email address of the restaurant.
        :ivar mobile: Contact number of the restaurant.
        :ivar address: Address of the restaurant.
        :ivar opening_time: Opening time of the restaurant.
        :ivar closing_time: Closing time of the restaurant.
        :ivar logo: Image file representing the restaurant's logo.
    """
    name: str
    email: str
    mobile: str
    address: str
    opening_time: str
    closing_time: str
    logo: UploadFile


class CreateItemSchema(BaseModel):
    """
        Schema representing data for creating an item.

        :ivar restaurant_id: ID of the restaurant to which the item belongs.
        :ivar name: Name of the item.
        :ivar description: Description of the item.
        :ivar cost: Cost of the item.
        :ivar price: Price of the item.
        :ivar is_active: Boolean indicating whether the item is active.
        :ivar image: Image file representing the item.
    """
    restaurant_id: int
    name: str
    description: str
    cost: float
    price: float
    is_active: bool
    image: UploadFile


class UpdateItemSchema(BaseModel):
    """
        Schema representing data for updating an item.

        :ivar name: Name of the item.
        :ivar description: Description of the item.
        :ivar cost: Cost of the item.
        :ivar price: Price of the item.
        :ivar is_active: Boolean indicating whether the item is active.
        :ivar image: Image file representing the item.
    """
    name: str
    description: str
    cost: float
    price: float
    is_active: bool
    image: UploadFile

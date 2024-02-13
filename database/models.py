import uuid
import datetime

from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import sqltypes

from . import constants
from .factory import BaseModel

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class User(BaseModel):
    __tablename__ = "users"

    name = Column(sqltypes.String(30), nullable=False)
    email = Column(sqltypes.String(50), unique=True, index=True)
    hashed_password = Column(sqltypes.String, nullable=False)
    role = Column(Enum(constants.UserRole), default=constants.UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)

    tokens = relationship("Token", back_populates="user")

    def save_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def varify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)


class Token(BaseModel):
    __tablename__ = "tokens"
    user_id = Column(sqltypes.Integer, ForeignKey("users.id"))
    token = Column(sqltypes.String(30), index=True, nullable=False)
    expiry = Column(sqltypes.DATETIME, nullable=False)

    user = relationship("User", back_populates="tokens")


class Restaurant(BaseModel):
    __tablename__ = "restaurants"
    user_id = Column(sqltypes.Integer, ForeignKey("users.id"))
    name = Column(sqltypes.String(30), nullable=False)
    email = Column(sqltypes.String(30), nullable=False)
    mobile = Column(sqltypes.String(30), nullable=False)
    address = Column(sqltypes.String(30), nullable=False)
    opening_time = Column(sqltypes.String(30))
    closing_time = Column(sqltypes.String(30))
    logo = Column(sqltypes.String(100), default='media/default.png')

    items = relationship("Item", back_populates="restaurant")


class Item(BaseModel):
    __tablename__ = "items"
    restaurant_id = Column(sqltypes.Integer, ForeignKey("restaurants.id"))
    name = Column(sqltypes.String(30), nullable=False)
    image = Column(sqltypes.String(100), default='media/default.png')
    description = Column(sqltypes.String)
    cost = Column(sqltypes.Numeric(precision=10, scale=2), nullable=False)
    price = Column(sqltypes.Numeric(precision=10, scale=2), nullable=False)
    is_active = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="items")

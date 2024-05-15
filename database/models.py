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
    """
        Model representing a user.

        This class defines attributes for user data such as name, email, hashed_password,
        role, and isActive. It also provides methods for password handling.

        :ivar name: Name of the user.
        :ivar email: Email address of the user.
        :ivar hashed_password: Hashed password of the user.
        :ivar role: Role of the user (default: CUSTOMER).
        :ivar is_active: Boolean indicating whether the user is active (default: True).
        :ivar tokens: Relationship with Token model.
    """
    __tablename__ = "users"

    name = Column(sqltypes.String(30), nullable=False)
    email = Column(sqltypes.String(50), unique=True, index=True)
    hashed_password = Column(sqltypes.String, nullable=False)
    role = Column(Enum(constants.UserRole), default=constants.UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)

    tokens = relationship("Token", back_populates="user")

    def save_password(self, password):

        """
            Hashes and saves the user's password.

            :param password: Password to be saved.
        """
        self.hashed_password = pwd_context.hash(password)


def varify_password(self, password):


    """
        Verifies the provided password against the stored hashed password.

        :param password: Password to be verified.
        :return: True if the password matches, otherwise False.
    """
    return pwd_context.verify(password, self.hashed_password)


class Token(BaseModel):
    """
        Model representing an authentication token.

        This class defines attributes for the authentication token, including the user ID,
        the token itself, and its expiry date.

        :ivar user_id: ID of the associated user.
        :ivar token: Authentication token.
        :ivar expiry: Expiry date of the token.
    """
    __tablename__ = "tokens"
    user_id = Column(sqltypes.Integer, ForeignKey("users.id"))
    token = Column(sqltypes.String(30), index=True, nullable=False)
    expiry = Column(sqltypes.DATETIME, nullable=False)

    user = relationship("User", back_populates="tokens")


class Restaurant(BaseModel):
    """
        Model representing a restaurant.

        This class defines attributes for restaurant data such as user_id, name, email,
        mobile, address, opening_time, closing_time, and logo.

        :ivar user_id: ID of the user owning the restaurant.
        :ivar name: Name of the restaurant.
        :ivar email: Email address of the restaurant.
        :ivar mobile: Contact number of the restaurant.
        :ivar address: Address of the restaurant.
        :ivar opening_time: Opening time of the restaurant.
        :ivar closing_time: Closing time of the restaurant.
        :ivar logo: URL to the restaurant's logo image.
        :ivar items: Relationship with Item model.
    """
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
    """
        Model representing an item.

        This class defines attributes for item data such as restaurant_id, name, image,
        description, cost, price, and isActive.

        :ivar restaurant_id: ID of the restaurant to which the item belongs.
        :ivar name: Name of the item.
        :ivar image: URL to the item's image.
        :ivar description: Description of the item.
        :ivar cost: Cost of the item.
        :ivar price: Price of the item.
        :ivar is_active: Boolean indicating whether the item is active.
        :ivar restaurant: Relationship with Restaurant model.
    """
    __tablename__ = "items"
    restaurant_id = Column(sqltypes.Integer, ForeignKey("restaurants.id"))
    name = Column(sqltypes.String(30), nullable=False)
    image = Column(sqltypes.String(100), default='media/default.png')
    description = Column(sqltypes.String)
    cost = Column(sqltypes.Numeric(precision=10, scale=2), nullable=False)
    price = Column(sqltypes.Numeric(precision=10, scale=2), nullable=False)
    is_active = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="items")

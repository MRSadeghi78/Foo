"""Python 3.11"""
import typing

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import crud, factory, schema
from database.schema import UserSchema


class CustomContext:
    """
    Custom context class used for dependency injection.

    This class is used to provide context containing user information
    and database session to route functions.

    Args:
        user (UserSchema): The user information associated with the current request.
        db (Session): The database session associated with the current request.
    """

    def __init__(self, user: schema.UserSchema, db: Session):
        """
        Initializes the CustomContext instance with user information and database session.

        Args:
            user (UserSchema): The user information associated with the current request.
            db (Session): The database session associated with the current request.
        """
        self._user = user
        self._db = db

    @property
    def user(self):
        return self._user

    @property
    def db(self):
        return self._db


async def get_token(request: Request):
    """
    Retrieves the authorization token from the request headers.

    :param request: Request object representing the incoming HTTP request.
    :return: Authorization token extracted from the request headers,
    or None if no valid token is found.
    """
    authorization: typing.Optional[str] = request.headers.get("Authorization")
    scheme, token = authorization.split() if authorization else (None, None)
    if scheme and scheme.lower() != "token":
        return None
    return token


async def verify_token(db, token_str):
    """
        Verifies the validity of an authorization token.

        :param db: Database session.
        :param token_str: Authorization token string to be verified.
        :return: User associated with the valid token.
        :raises HTTPException 401: If the token is missing or invalid.
    """
    if not token_str:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = crud.get_user_by_token(db, token_str)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token.user


async def get_current_user(
        db: Session = Depends(factory.get_db), token_str=Depends(get_token),
) -> CustomContext:
    """
      Retrieves the current user based on the provided authorization token.

      :param db: Database session.
      :param token_str: Authorization token string.
      :return: CustomContext containing user information.
    """
    user = await verify_token(db, token_str)
    return CustomContext(UserSchema(**{k: v for k, v in vars(user).items()}), db)

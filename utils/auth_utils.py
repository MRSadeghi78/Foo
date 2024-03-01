from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import crud
from database.factory import get_db
from database.schema import UserSchema


class CustomContext:
    def __init__(self, user: UserSchema, db: Session):
        self.user = user
        self.db = db


async def get_token(request: Request):
    authorization: Optional[str] = request.headers.get("Authorization")
    scheme, token = authorization.split() if authorization else (None, None)
    if scheme and scheme.lower() != "token":
        return None
    return token


async def verify_token(db, token_str):
    if not token_str:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = crud.get_user_by_token(db, token_str)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token.user


async def get_current_user(db: Session = Depends(get_db), token_str=Depends(get_token), ) -> CustomContext:
    user = await verify_token(db, token_str)
    return CustomContext(UserSchema(**{k: v for k, v in vars(user).items()}), db)

import datetime
import uuid

from sqlalchemy.orm import Session

from . import models, schema


# User related operation
def get_user(db: Session, user_id: int):
    return db.query(models.User).get(models.User.id == user_id)


def get_user_by_token(db: Session, token_str: str):
    return db.query(models.Token).filter(models.Token.token == token_str).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Token related operation
def add_token(db: Session, user_id: int):
    token = db.query(models.Token).filter(
        models.Token.user_id == user_id,
        models.Token.expiry > datetime.datetime.utcnow()
    ).first()
    if not token:
        token = models.Token(
            user_id=user_id,
            token=uuid.UUID(str(uuid.uuid4())).hex,
            expiry=datetime.datetime.utcnow() + datetime.timedelta(days=14)
        )
        db.add(token)
        db.commit()
        db.refresh(token)
    return token


# Restaurant related operation
def get_restaurant(db: Session, user_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.user_id == user_id).first()


def update_restaurant(db: Session, user_id: int, data: schema.RestaurantSchema):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.user_id == user_id).first()
    if restaurant:
        for key, value in data.dict().items():
            setattr(restaurant, key, value)
    else:
        restaurant = models.Restaurant(**data.dict(), user_id=user_id)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


# Item related operation
def get_items(db: Session, restaurant_id: int):
    return db.query(models.Item).filter(models.Item.restaurant_id == restaurant_id).all()


def create_item(db: Session, data: schema.CreateItemSchema):
    item = models.Item(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item_id: int, data: schema.UpdateItemSchema):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        return None
    for key, value in data.dict().items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

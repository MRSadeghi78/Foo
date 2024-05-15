import datetime
import uuid

from sqlalchemy.orm import Session

from . import models, schema


# User related operation
def get_user(db: Session, user_id: int):
    """
        Retrieves a user by user ID.

        :param db: Database session.
        :param user_id: ID of the user to retrieve.
        :return: User object if found, otherwise None.
    """
    return db.query(models.User).get(models.User.id == user_id)


def get_user_by_token(db: Session, token_str: str):
    """
        Retrieves a user by token.

        :param db: Database session.
        :param token_str: Token string associated with the user.
        :return: User object if found, otherwise None.
    """
    # noinspection PyTypeChecker
    return db.query(models.Token).filter(models.Token.token == token_str).first()


def get_user_by_email(db: Session, email: str):
    """
        Retrieves a user by email.

        :param db: Database session.
        :param email: Email address of the user to retrieve.
        :return: User object if found, otherwise None.
    """
    # noinspection PyTypeChecker
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
       Retrieves a list of users with optional pagination.

       :param db: Database session.
       :param skip: Number of records to skip.
       :param limit: Maximum number of records to retrieve.
       :return: List of user objects.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


# Token related operation
def add_token(db: Session, user_id: int):
    """
       Adds a token for a user.

       :param db: Database session.
       :param user_id: ID of the user for whom the token is being added.
       :return: Token object.
    """
    # noinspection PyTypeChecker
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
    """
        Retrieves a restaurant by user ID.

        :param db: Database session.
        :param user_id: ID of the user owning the restaurant.
        :return: Restaurant object if found, otherwise None.
    """
    # noinspection PyTypeChecker
    return db.query(models.Restaurant).filter(models.Restaurant.user_id == user_id).first()


# Restaurant related operation
def get_restaurant_by_id(db: Session, restaurant_id: int):
    """
        Retrieves a restaurant by restaurant ID.

        :param db: Database session.
        :param restaurant_id: ID of the restaurant.
        :return: Restaurant object if found, otherwise None.
    """
    # noinspection PyTypeChecker
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()


def update_restaurant(db: Session, user_id: int, data: schema.RestaurantSchema):
    """
        Updates or creates a restaurant.

        :param db: Database session.
        :param user_id: ID of the user owning the restaurant.
        :param data: Data to update or create the restaurant.
        :return: Updated or created restaurant object.
    """
    # noinspection PyTypeChecker
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
    """
        Retrieves items for a restaurant.

        :param db: Database session.
        :param restaurant_id: ID of the restaurant.
        :return: List of item objects.
    """
    # noinspection PyTypeChecker
    return db.query(models.Item).filter(models.Item.restaurant_id == restaurant_id).all()


def create_item(db: Session, data: schema.CreateItemSchema):
    """
       Creates an item.

       :param db: Database session.
       :param data: Data to create the item.
       :return: Created item object.
    """
    item = models.Item(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item_id: int, data: schema.UpdateItemSchema):
    """
        Updates an item.

        :param db: Database session.
        :param item_id: ID of the item to update.
        :param data: Data to update the item.
        :return: Updated item object if found, otherwise None.
    """
    # noinspection PyTypeChecker
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
    """
        Deletes an item.

        :param db: Database session.
        :param item_id: ID of the item to delete.
        :return: True if item was deleted successfully, otherwise False.
    """
    # noinspection PyTypeChecker
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def delete_all_item(db: Session):
    """
        Deletes all the items.

        :param db: Database session.
        :return: True if all items were deleted successfully, otherwise False.
    """
    items = db.query(models.Item).all()
    for item in items:
        db.delete(item)
    db.commit()
    return True

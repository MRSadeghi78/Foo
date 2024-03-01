from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int
    created_at: datetime = None
    updated_at: datetime = None


class LoginResponseSchema(BaseSchema):
    user_id: int
    token: str
    expiry: datetime

    class Config:
        from_attributes = True


class RestaurantResponseSchema(BaseSchema):
    user_id: int
    name: str
    email: str
    mobile: str
    address: str
    opening_time: str
    closing_time: str
    logo: str

    class Config:
        from_attributes = True


class ItemResponseSchema(BaseSchema):
    restaurant_id: int
    name: str
    description: str
    cost: float
    price: float
    is_active: bool
    image: str

    class Config:
        from_attributes = True

from datetime import datetime

from pydantic import BaseModel, computed_field
from typing import Dict


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

    @computed_field
    def links(self) -> Dict[str, str]:
        return {
            "self": f"/api/restaurant/",
            "items-collection": f"/api/items/{self.restaurant_id}/"
        }


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

    @computed_field
    def links(self) -> Dict[str, str]:
        return {
            "self": f"/api/items/{self.id}/",
            "items-collection": f"/api/items/{self.restaurant_id}/",
            "restaurant": f"/api/restaurant/"
        }

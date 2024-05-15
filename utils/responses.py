from datetime import datetime
from typing import Dict

from pydantic import BaseModel, computed_field


class BaseSchema(BaseModel):
    """
        Base schema representing common fields for database entities.

        :param id: Unique identifier for the entity.
        :param created_at: Date and time when the entity was created.
        :param updated_at: Date and time when the entity was last updated.
    """
    id: int
    created_at: datetime = None
    updated_at: datetime = None


class LoginResponseSchema(BaseSchema):
    """
        Schema representing the response to a login request.

        Inherits from BaseSchema.

        :param user_id: Unique identifier for the user.
        :param token: Authentication token.
        :param expiry: Date and time when the token expires.
    """
    user_id: int
    token: str
    expiry: datetime

    class Config:
        from_attributes = True


class RestaurantResponseSchema(BaseSchema):
    """
        Schema representing a restaurant response.

        Inherits from BaseSchema.

        :param user_id: Unique identifier for the user.
        :param name: Name of the restaurant.
        :param email: Email address of the restaurant.
        :param mobile: Contact number of the restaurant.
        :param address: Address of the restaurant.
        :param opening_time: Opening time of the restaurant.
        :param closing_time: Closing time of the restaurant.
        :param logo: URL to the restaurant's logo image.
    """
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
        """
        Computes and returns a dictionary containing links associated with the current object.

        This computed field generates links for REST API resources related to the current object.

        Returns:
            Dict[str, str]: A dictionary containing links, where keys represent link names and values represent URLs.
        """
        return {
            "self": f"/api/restaurant/",
            "items-collection": f"/api/items/{self.id}/"
        }


class ItemResponseSchema(BaseSchema):
    """
    Schema representing an item response.

    Inherits from BaseSchema.

    :param restaurant_id: Unique identifier for the restaurant.
    :param name: Name of the item.
    :param description: Description of the item.
    :param cost: Cost of the item.
    :param price: Price of the item.
    :param is_active: Indicates whether the item is active.
    :param image: URL to the item's image.
    """
    restaurant_id: int
    name: str
    description: str
    cost: float
    price: float
    is_active: bool
    image: str

    class Config:
        """
            Configuration settings for ItemResponseSchema.
            Enables conversion from attribute names to snake_case during serialization.
        """
        from_attributes = True

    @computed_field
    def links(self) -> Dict[str, str]:
        """
                Computes and returns links related to the restaurant.
                :return: Dictionary containing links.
            """
        return {
            "self": f"/api/items/{self.id}/",
            "items-collection": f"/api/items/{self.restaurant_id}/",
            "restaurant": f"/api/restaurant/"
        }

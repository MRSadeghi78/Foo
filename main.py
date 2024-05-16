"""Python 3.11"""
from typing import List, Any

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError, parse_obj_as
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import schema, crud, helper
from database.factory import engine, Base, get_db
from utils import auth_utils, image_utils, responses, swagger, auxiliary_service

origins = [
    "*"
]

app = FastAPI()
app.openapi = swagger.generate_custom_openapi
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    """
    Function executed on application startup.
    This function creates all database tables defined in the Base metadata binding to the engine.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    """
       Root endpoint of the API.

       This endpoint creates a user in the database on the first call.
       If the user already exists, it simply returns a greeting message.

       :param db: Database session.
       :return: Greeting message.
    """
    try:
        helper.create_user(db)
    except SQLAlchemyError:
        pass
    return {"msg": "Hello "}


@app.post("/auth/login/")
async def login(
        data: schema.LoginSchema,
        db: Session = Depends(get_db)
) -> responses.LoginResponseSchema:
    """
       Endpoint for user login.

       This endpoint authenticates a user by email and password.
       If authentication is successful, it returns a token response schema.
       Otherwise, it raises a 400 HTTPException with a message indicating invalid credentials.

       :param data: Login credentials.
       :param db: Database session.
       :return: Token response schema.
    """
    user = crud.get_user_by_email(db, data.email)
    if user and user.varify_password(data.password):
        token = crud.add_token(db, user.id)
        return responses.LoginResponseSchema.from_orm(token)
    raise HTTPException(status_code=400, detail="Invalid credentials")


@app.get("/restaurant/")
async def get_restaurant(
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.RestaurantResponseSchema:
    """
        Endpoint to retrieve restaurant details.

        This endpoint retrieves details of the restaurant associated with the authenticated user.
        If no restaurant is found, it raises a 404 HTTPException.

        :param context: Custom context containing user information.
        :return: Restaurant response schema containing restaurant details.
    """
    restaurant = crud.get_restaurant(context.db, context.user.id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="No data found")
    return responses.RestaurantResponseSchema.from_orm(restaurant)


@app.put("/restaurant/", openapi_extra=swagger.generate_form_input(schema.RestaurantSchema))
async def update_restaurant(
        request: Request,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.RestaurantResponseSchema:
    """
    Endpoint to update restaurant details.

    This endpoint allows the authenticated user to update their restaurant details.
    It expects a form containing restaurant data.
    Upon successful update, it returns the updated restaurant details.

    If the provided data is invalid, it raises a 400 HTTPException.
        :param request: Request object containing form data.
        :param context: Custom context containing user information.
        :return: Updated restaurant response schema.
    """
    form = await request.form()
    try:
        data = schema.RestaurantSchema(**form)
        data.logo = image_utils.save_image(data.logo, 'logo')
        restaurant = crud.update_restaurant(context.db, context.user.id, data)
        return responses.RestaurantResponseSchema.from_orm(restaurant)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.get("/items/{restaurant_id}/")
async def get_items(
        restaurant_id: int,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> list[responses.ItemResponseSchema]:
    """
        Endpoint to retrieve items for a specific restaurant.

        This endpoint retrieves items associated with the specified restaurant ID.
        It expects an authenticated user and returns a list of item response schemas.
        If no items are found for the given restaurant ID, an empty list is returned.

        :param restaurant_id: ID of the restaurant.
        :param context: Custom context containing user information.
        :return: List of item response schemas.
    """
    restaurant = crud.get_restaurant_by_id(context.db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Invalid Restaurant ID")
    items = crud.get_items(context.db, restaurant_id)
    return parse_obj_as(List[responses.ItemResponseSchema], items)


@app.post("/items/", openapi_extra=swagger.generate_form_input(schema.CreateItemSchema))
async def create_item(
        request: Request,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.ItemResponseSchema:
    """
        Endpoint to create a new item.

        This endpoint allows an authenticated user to create a new item.
        It expects form data containing item details.
        Upon successful creation, it returns the created item response schema.
        If the provided data is invalid, it raises a 400 HTTPException.

        :param request: Request object containing form data.
        :param context: Custom context containing user information.
        :return: Created item response schema.
    """
    form = await request.form()
    try:
        data = schema.CreateItemSchema(**form)
        data.image = image_utils.save_image(data.image, 'image')
        item = crud.create_item(context.db, data)
        return responses.ItemResponseSchema.from_orm(item)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.put("/items/{item_id}/", openapi_extra=swagger.generate_form_input(schema.UpdateItemSchema))
async def update_item(
        item_id: int, request: Request,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.ItemResponseSchema:
    """
       Endpoint to update an existing item.

       This endpoint allows an authenticated user to update an existing item.
       It expects form data containing updated item details.
       Upon successful update, it returns the updated item response schema.
       If the provided data is invalid or the item is not found,
       it raises a 400 or 404 HTTPException respectively.

       :param item_id: ID of the item to be updated.
       :param request: Request object containing form data.
       :param context: Custom context containing user information.
       :return: Updated item response schema.
    """
    form = await request.form()
    try:
        data = schema.UpdateItemSchema(**form)
        data.image = image_utils.save_image(data.image, 'image')
        item = crud.update_item(context.db, item_id, data)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return responses.ItemResponseSchema.from_orm(item)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.delete("/items/all/")
async def delete_all_item(
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> Any:
    """
        Endpoint to delete an existing item.

        This endpoint allows an authenticated user to delete all the items from db.
        Upon successful deletion, it returns a success message.
        If the item is not found, it raises a 404 HTTPException.

        :param context: Custom context containing user information.
        :return: Success message upon deletion.
    """
    is_success = crud.delete_all_item(context.db)
    if is_success:
        return {"detail": "All items deleted successfully"}
    raise HTTPException(status_code=500, detail="Error while deleting items")


@app.delete("/items/{item_id}/")
async def delete_item(
        item_id: int,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> Any:
    """
        Endpoint to delete an existing item.

        This endpoint allows an authenticated user to delete an existing item by its ID.
        Upon successful deletion, it returns a success message.
        If the item is not found, it raises a 404 HTTPException.

        :param item_id: ID of the item to be deleted.
        :param context: Custom context containing user information.
        :return: Success message upon deletion.
    """
    is_success = crud.delete_item(context.db, item_id)
    if is_success:
        return {"detail": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/location/")
async def get_location(
        request: Request
) -> Any:
    """
        Endpoint to retrieve location data based on IP address.

        This endpoint retrieves location data based on the client's IP address.
        If the location data is available, it is returned.
        If the auxiliary service is unavailable, it raises a 503 HTTPException.

        :param request: Request object containing client's IP address.
        :return: Location data if available.
    """
    ip_address = auxiliary_service.get_client_ip(request)
    data = auxiliary_service.ip_to_location(ip_address)
    if data:
        return data
    raise HTTPException(status_code=503, detail="Auxiliary service is not available")

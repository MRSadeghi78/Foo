from typing import List, Any

from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import ValidationError, parse_obj_as
from sqlalchemy.orm import Session

from database import schema, crud, helper
from database.factory import engine, Base, get_db
from utils import auth_utils, image_utils, responses, swagger, auxiliary_service

app = FastAPI()
app.openapi = swagger.generate_custom_openapi


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    try:
        helper.create_user(db)
    except Exception as e:
        pass
    return {"msg": "Hello "}


@app.post("/auth/login/")
async def login(
        data: schema.LoginSchema,
        db: Session = Depends(get_db)
) -> responses.LoginResponseSchema:
    user = crud.get_user_by_email(db, data.email)
    if user and user.varify_password(data.password):
        token = crud.add_token(db, user.id)
        return responses.LoginResponseSchema.from_orm(token)
    raise HTTPException(status_code=400, detail="Invalid credentials")


@app.get("/restaurant/")
async def get_restaurant(
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.RestaurantResponseSchema:
    restaurant = crud.get_restaurant(context.db, context.user.id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="No data found")
    return responses.RestaurantResponseSchema.from_orm(restaurant)


@app.post("/restaurant/", openapi_extra=swagger.generate_form_input(schema.RestaurantSchema))
async def update_restaurant(
        request: Request,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.RestaurantResponseSchema:
    form = await request.form()
    try:
        data = schema.RestaurantSchema(**form)
        data.logo = image_utils.save_image(data.logo, 'logo')
        restaurant = crud.update_restaurant(context.db, context.user.id, data)
        return responses.RestaurantResponseSchema.from_orm(restaurant)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.get("/items/{restaurant_id}/")
async def get_items(
        restaurant_id: int,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> list[responses.ItemResponseSchema]:
    items = crud.get_items(context.db, restaurant_id)
    return parse_obj_as(List[responses.ItemResponseSchema], items)


@app.post("/items/", openapi_extra=swagger.generate_form_input(schema.CreateItemSchema))
async def create_item(
        request: Request,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.ItemResponseSchema:
    form = await request.form()
    try:
        data = schema.CreateItemSchema(**form)
        data.image = image_utils.save_image(data.image, 'image')
        item = crud.create_item(context.db, data)
        return responses.ItemResponseSchema.from_orm(item)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.put("/items/{item_id}/", openapi_extra=swagger.generate_form_input(schema.UpdateItemSchema))
async def update_item(
        item_id: int, request: Request,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> responses.ItemResponseSchema:
    form = await request.form()
    try:
        data = schema.UpdateItemSchema(**form)
        data.image = image_utils.save_image(data.image, 'image')
        item = crud.update_item(context.db, item_id, data)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return responses.ItemResponseSchema.from_orm(item)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid data")


@app.delete("/items/{item_id}/")
async def delete_item(
        item_id: int,
        context: auth_utils.CustomContext = Depends(auth_utils.get_current_user)
) -> Any:
    is_success = crud.delete_item(context.db, item_id)
    if is_success:
        return {"detail": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/location/")
async def get_location(
        request: Request
) -> Any:
    ip_address = auxiliary_service.get_client_ip(request)
    data = auxiliary_service.ip_to_location(ip_address)
    if data:
        return data
    raise HTTPException(status_code=503, detail="Auxiliary service is not available")

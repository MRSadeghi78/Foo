from fastapi import FastAPI
from database.factory import engine
from database import models

app = FastAPI()


@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

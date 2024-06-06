from fastapi import APIRouter, HTTPException

routes = APIRouter()


@routes.get("/")
async def root():
    return {"message": "Hello World"}


@routes.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
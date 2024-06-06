from fastapi import APIRouter, HTTPException

routes = APIRouter()


@routes.get("/2")
async def root():
    return {"message": "Hello World 2"}


@routes.get("/hello/{name}/2")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

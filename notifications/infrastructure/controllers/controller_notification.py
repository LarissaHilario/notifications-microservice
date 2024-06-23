from fastapi import APIRouter, HTTPException

routes = APIRouter()


@routes.get("/health")
async def root():
    return {"message": "OK"}

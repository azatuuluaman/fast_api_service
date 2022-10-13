from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from user.schemas.schemas import CreateUser
from user.database.db import client

router = APIRouter()
db = client.users


@router.post(
    "/signUp", response_description="register new user", response_model=CreateUser
)
async def register(user: CreateUser = Body(...)):
    if not user.is_valid():
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content="Passwords do not match"
        )

    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

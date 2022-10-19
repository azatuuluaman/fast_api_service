from fastapi import APIRouter, Body, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from user.schemas.schemas import CreateUser, SignInUser, GetUser
from user.database.db import client
from user.modules.deps import get_current_user
from user.modules.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)

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


@router.post("/signIn", response_description="login user", response_model=SignInUser)
async def login(user: SignInUser = Body(...)):
    user = jsonable_encoder(user)
    get_user = await db["users"].find_one({"email": user.get("email")})

    if get_user is None :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = get_hashed_password(get_user.get("password"))

    if not verify_password(user.get("password"), hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": create_access_token(user.get("email")),
            "refresh_token": create_refresh_token(user.get("email")),
        },
    )


@router.get(
    "/me", summary="Get details of currently logged in user", response_model=GetUser
)

async def get_me(user: GetUser = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

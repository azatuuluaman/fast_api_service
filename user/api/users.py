from fastapi import APIRouter, Body, status, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from user.schemas.schemas import CreateUser, SignInUser, GetUser
from user.database.db import client
from user.modules.deps import get_current_user
from user.modules.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    get_random_string,
    verify_password,
    get_code_by_email,
    get_redis,
    send_code,
)

router = APIRouter()
db = client.users


@router.get(
    "/activate/{id}", response_description="activate user", response_model=CreateUser
)
async def activate(id: str, activate_code: str):
    user = await db["users"].find_one({"_id": id})
    email = user.get("email")
    code = get_code_by_email(email)
    if code != activate_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect activation code"
        )

    updated_user = await db.users.update_one({"_id": id}, {"$set": {"is_active": True}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_user)


@router.post(
    "/signUp", response_description="register new user", response_model=CreateUser
)
async def register(user: CreateUser = Body(...)):
    if not user.is_valid():
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content="Passwords do not match"
        )

    user = jsonable_encoder(user)
    inserted_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": inserted_user.inserted_id})
    code = get_random_string(6)
    email = user.get("email")
    with get_redis() as r:
        r.set(email, code)

    send_code(email, code)
    return JSONResponse(content=created_user, status_code=status.HTTP_200_OK)


@router.post("/signIn", response_description="login user", response_model=SignInUser)
async def login(user: SignInUser = Body(...)):
    user = jsonable_encoder(user)
    get_user = await db["users"].find_one({"email": user.get("email")})

    if get_user is None:
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


@router.put("/", summary="update currently logged in user")
async def update_user(user: GetUser, current_user: GetUser = Depends(get_current_user)):
    user = {k: v for k, v in user.dict().items() if v is not None and k != "id"}

    if len(user) >= 1:
        update_result = await db["users"].update_one(
            {"email": current_user.get("email")}, {"$set": user}
        )
        if update_result.modified_count == 1:
            if (
                    updated_user := await db["users"].find_one(
                        {"email": current_user.get("email")}
                    )
            ) is not None:
                return updated_user

    if (
            existing_user := await db["users"].find_one(
                {"email": current_user.get("email")}
            )
    ) is not None:
        return existing_user

    raise HTTPException(
        status_code=404, detail=f"User {current_user.get('email')} not found"
    )

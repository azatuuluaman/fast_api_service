from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from user.modules.utils import ALGORITHM, JWT_SECRET_KEY

from jose import jwt
from pydantic import ValidationError
from user.schemas.schemas import GetUser, TokenPayload
from user.database.db import client

db = client.users

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/signIn", scheme_name="JWT")


async def get_current_user(token: str = Depends(reuseable_oauth)) -> GetUser:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

        token_data = TokenPayload(**payload)
        print(token_data.exp)
        print(token_data.sub)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db["users"].find_one({"email": token_data.get("sub")})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user

from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from advert.database.db import client
from user.database.db import client as user_client
from user.schemas.schemas import GetUser
from advert.schemas.schemas import AdvertBase, AdvertUpdate
from user.modules.deps import get_current_user

router = APIRouter()
advert_db = client.adverts
user_db = user_client.users


@router.get("/", response_model=List[AdvertBase])
async def get_adverts(limit: int = 50):
    adverts = await advert_db["advert"].find().to_list(limit)
    return adverts


@router.post("/", response_model=AdvertBase)
async def create_advert(advert: AdvertBase, user: GetUser = Depends(get_current_user)):
    advert = jsonable_encoder(advert)
    new_advert = await advert_db["advert"].insert_one(advert)
    created_advert = await advert_db["advert"].find_one({"_id": new_advert.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_advert)


@router.put("/{id}", response_model=AdvertBase)
async def update_advert(
    id: str, advert: AdvertUpdate, user: GetUser = Depends(get_current_user)
):
    advert = {k: v for k, v in advert.dict().items() if v is not None}
    if (current_advert := await advert_db["advert"].find_one({"_id": id})) is None:
        raise HTTPException(status_code=404, detail=f"advert {id} not found")

    await advert_db.advert.update_one({"_id": id}, {"$set": advert})
    get_updated = await advert_db.advert.find_one({"_id": id})
    return get_updated

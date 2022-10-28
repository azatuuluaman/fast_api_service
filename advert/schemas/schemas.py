from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
from user.schemas.schemas import PyObjectId


class AdvertStatus(str, Enum):
    """Choices for advert status"""

    active = "Активный"
    inactive = "Неактивный"
    on_review = "На проверке"


class AdvertPromote(str, Enum):
    vip = "VIP"
    urgently = "Срочно"
    highlighted = "Выделить"


class AdvertBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner: str
    title: str
    description: str
    category: str
    sub_category: str
    price: str
    status: str = AdvertStatus.inactive
    promote: Optional[AdvertPromote]
    city: str
    end_price: Optional[str]
    email: EmailStr
    wa_number: str
    photo: Optional[List[str]]

    class Config:
        json_encoders = {ObjectId: str}

        schema_extra = {
            "example": {
                "owner": "Jane",
                "title": "example_title",
                "email": "jdoe@example.com",
                "wa_number": "+996999312292",
                "description": "example description",
                "category": "example category",
                "sub_category": "example child_category",
                "city": "example city",
                "price": "1000 KGS",
                "end_price": "1500 KGS",
                "status": "Неактивный",
                "promote": "VIP",
            }
        }


class AdvertUpdate(BaseModel):
    owner: Optional[str]
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    sub_category: Optional[str]

    price: Optional[str]

    status: Optional[AdvertStatus]
    promote: Optional[AdvertPromote]
    city: Optional[str]
    end_price: Optional[str]
    email: Optional[EmailStr]
    wa_number: Optional[str]

    class Config:
        json_encoders = {ObjectId: str}

        schema_extra = {
            "example": {
                "owner": "Jane",
                "title": "example_title",
                "email": "jdoe@example.com",
                "wa_number": "+996999312292",
                "description": "example description",
                "category": "example category",
                "sub_category": "example child_category",
                "city": "example city",
                "price": "1000 KGS",
                "end_price": "1500 KGS",
                "status": "Неактивный",
                "promote": "VIP",
            }
        }

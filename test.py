from pydantic import BaseModel, Field, ValidationError
from enum import Enum


class Advert(BaseModel):
    class AdvertType(str, Enum):
        BUY = "buy"
        SELL = "sell"

    advert_type: AdvertType = Field(..., alias="type")
    price: float = Field(..., alias="price")
    amount: float = Field(..., alias="amount")
    total: float = Field(..., alias="total")


a = Advert(type="buy", price=100.3, amount=1000.3, total=10000.3)
print(a.dict())

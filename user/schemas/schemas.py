from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    __tablename__ = 'users'
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: str = Field(...)


class CreateUser(User):
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...)
    password: str = Field(...)

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jdoe@example.com",
                "phone_number": "+996999312292",
                "password": "admin12345"
            }
        }


class SignInUser(User):
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "jdoe@example.com",
            }
        }



class UpdateUser(User):
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...)
    old_password: Optional[str] = ''
    new_password: Optional[str] = ''

    class Config:
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jdoe@example.com",
                "phone_number": "+996123123123",
            }
        }



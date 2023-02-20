from datetime import datetime
from typing import Optional, List

from pydantic import validator
from pydantic.main import BaseModel
from pydantic.types import UUID4

from src.base.schema import BaseResponse
from src.modules.user.model import User


class UserSchemaIn(BaseModel):
    name: str
    email: str
    identity_id: str

    @validator('email')
    def validate_email(cls, value):
        if User.get_by_email(value):
            raise ValueError('email already registered')
        return value

    @validator('identity_id')
    def validate_identity_id(cls, value):
        if User.get_by_identity(value):
            raise ValueError('Identity already registered')
        return value


class UserSchemaUpdateIn(BaseModel):
    name: Optional[str]
    email: Optional[str]
    identity_id: Optional[str]

    @validator('email')
    def validate_email(cls, value):
        if User.get_by_email(value):
            raise ValueError('email already registered')
        return value

    @validator('identity_id')
    def validate_identity_id(cls, value):
        if User.get_by_identity(value):
            raise ValueError('Identity already registered')
        return value


class UserSchema(BaseModel):
    id: UUID4
    name: str
    email: Optional[str]
    identity_id: Optional[str]
    createdat: Optional[datetime]
    updatedat: Optional[datetime]

    class Config:
        orm_mode = True


class UserListResponse(BaseResponse):
    result: List[UserSchema]


class UserResponse(BaseResponse):
    result: UserSchema

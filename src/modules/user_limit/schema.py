from datetime import datetime
from typing import List, Optional

from pydantic import validator
from pydantic.main import BaseModel
from pydantic.types import UUID4

from src.base.schema import BaseResponse
from src.modules.master_limit.model import MLimit
from src.modules.user.model import User


class UserLimitSchemaIn(BaseModel):
    user_id: str
    limit_id: str
    limit_total: Optional[int] = 0
    limit_balance: Optional[int] = 0
    outstanding_balance: Optional[int] = 0

    @validator('user_id')
    def validate_user_id(cls, value):
        if not User.get(value):
            raise ValueError('user not found')
        return value


class UserlimitSchemaUpdateIn(BaseModel):
    user_id: str
    limit_id: str
    limit_total: Optional[int] = 0
    limit_balance: Optional[int] = 0
    outstanding_balance: Optional[int] = 0

    @validator('user_id')
    def validate_user(cls, value):
        if not User.get(value):
            raise ValueError('user not found')
        return value


class UserLimitSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    limit_id: UUID4
    limit_duration: str
    limit_total: Optional[int] = 0
    limit_balance: Optional[int] = 0
    outstanding_balance: Optional[int] = 0
    createdat: Optional[datetime]
    updatedat: Optional[datetime]

    class Config:
        orm_mode = True


class UserLimitListResponse(BaseResponse):
    result: List[UserLimitSchema]


class UserLimitResponse(BaseResponse):
    result: UserLimitSchema

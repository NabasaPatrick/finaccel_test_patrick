from datetime import datetime
from typing import Optional, List

from pydantic import validator
from pydantic.main import BaseModel
from pydantic.types import UUID4

from src.base.schema import BaseResponse
from src.modules.loan.model import Loan
from src.modules.user.model import User


class PaymentSchemaIn(BaseModel):
    loan_id: UUID4
    user_id: UUID4
    amount: Optional[int]

    @validator('loan_id')
    def validate_loan_id(cls, value):
        if not Loan.get(value):
            raise ValueError('Loan not found')
        return value

    @validator('user_id')
    def validate_user_id(cls, value):
        if not User.get(value):
            raise ValueError('User  not found')
        return value


class PaymentSchemaUpdateIn(BaseModel):
    loan_id: UUID4
    user_id: UUID4
    status: Optional[str]
    amount: Optional[int]

    @validator('loan_id')
    def validate_loan_id(cls, value):
        if not Loan.get(value):
            raise ValueError('Loan not found')
        return value

    @validator('user_id')
    def validate_user_id(cls, value):
        if not User.get(value):
            raise ValueError('User  not found')
        return value


class PaymentSchema(BaseModel):
    id: UUID4
    loan_id: UUID4
    user_id: UUID4
    amount: Optional[int]
    createdat: Optional[datetime]

    class Config:
        orm_mode = True


class PaymentListResponse(BaseResponse):
    result: List[PaymentSchema]


class PaymentResponse(BaseResponse):
    result: PaymentSchema

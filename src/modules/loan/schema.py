from datetime import datetime
from typing import Optional, List

from pydantic import validator, UUID4
from pydantic.main import BaseModel

from src.base.schema import BaseResponse
from src.modules.loan.model import Loan
from src.modules.user_limit.model import UserLimit


class LoanSchemaIn(BaseModel):
    user_limit: UUID4
    total_loan: Optional[int]

    @validator('user_limit')
    def validate_user_limit(cls, value):
        if not UserLimit.get(value):
            raise ValueError('User Limit not found')
        return value


class LoanSchema(BaseModel):
    id: UUID4
    user_limit: UUID4
    start_date: Optional[datetime]
    est_end_date: Optional[datetime]
    next_payment_date: Optional[datetime]
    last_payment_date: Optional[datetime]
    loan_tenur: Optional[int]
    total_loan: Optional[int]
    total_paid: Optional[int]
    emi_amt: Optional[int]
    status: Optional[str]

    createdat: Optional[datetime]
    updatedat: Optional[datetime]

    class Config:
        orm_mode = True


class LoanInfoSchema(BaseModel):
    id: UUID4
    user_limit: UUID4
    status: Optional[str]
    next_payment_date: Optional[datetime]
    is_late: bool = False
    total_loan: Optional[int]
    bill: Optional[int]


class LoanListResponse(BaseResponse):
    result: List[LoanSchema]


class LoanResponse(BaseResponse):
    result: LoanSchema


class LoanInfoResponse (BaseResponse):
    result = LoanInfoSchema
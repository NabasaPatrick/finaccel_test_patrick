import enum
from datetime import datetime
from typing import Optional, List

from pydantic.main import BaseModel
from pydantic.types import UUID4

from src.base.schema import BaseResponse


class DurationType(str, enum.Enum):
    Day = "Day"
    Month = "Month"


class MLimitSchemaIn(BaseModel):
    limit_duration: Optional[str]
    duration_type: DurationType


class MLimitSchemaUpdateIn(BaseModel):
    limit_duration: Optional[str]
    duration_type: DurationType


class MLimitSchema(BaseModel):
    id: UUID4
    limit_duration: Optional[str]
    duration_type: Optional[str]
    createdat: Optional[datetime]
    updatedat: Optional[datetime]

    class Config:
        orm_mode = True


class MLimitListResponse(BaseResponse):
    result: List[MLimitSchema]


class MLimitResponse(BaseResponse):
    result: MLimitSchema

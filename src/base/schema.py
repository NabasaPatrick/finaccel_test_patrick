from typing import Optional, Any

from pydantic.main import BaseModel


class BaseResponse(BaseModel):
    success: bool = True
    meta: Optional[Any]
    result: Optional[Any]
    message: Optional[str]
    errors: Optional[dict] = None
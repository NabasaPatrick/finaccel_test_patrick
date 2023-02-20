from fastapi import APIRouter, Query
from fastapi_sqlalchemy import db
from starlette import status

from src.modules.master_limit.helpers import get_mlimits, get_mlimit_count, add_mlimit, update_mlimit
from src.modules.master_limit.model import MLimit
from src.modules.master_limit.schema import MLimitResponse, MLimitSchemaUpdateIn, MLimitSchemaIn, MLimitListResponse

router = APIRouter(prefix='/m_limit', tags=['Master Limit'])


@router.get("", response_model=MLimitListResponse)
def get_mlimit(search: str = Query(None)):
    mlimits = get_mlimits(search)
    count = get_mlimit_count(search)
    return MLimitListResponse.parse_obj({
            'result': mlimits,
            'meta': {
                'count': count
            }
        })


@router.post("", response_model=MLimitResponse)
def post_mlimit(data: MLimitSchemaIn):
    mlimit = add_mlimit(data)
    return MLimitResponse(result=mlimit)


@router.patch("", response_model=MLimitResponse)
def patch_mlimit(id: str, data: MLimitSchemaUpdateIn):
    exist_mlimit = MLimit.get(id)
    mlimit = update_mlimit(exist_mlimit, data)
    return MLimitResponse(result=mlimit)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_mlimit(id: str):
    exist_mlimit = MLimit.get(id)
    db.session.delete(exist_mlimit)
    db.session.commit()
    return

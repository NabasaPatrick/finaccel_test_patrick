from typing import Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi_sqlalchemy import db
from starlette import status

from src.modules.user.schema import UserResponse
from src.modules.user_limit.helpers import get_user_limits, get_user_limit_count, update_user_limit
from src.modules.user_limit.model import UserLimit
from src.modules.user_limit.schema import UserLimitListResponse, UserlimitSchemaUpdateIn

from src.modules.user_limit.helpers import add_user_limit
from src.modules.user_limit.schema import UserLimitResponse, UserLimitSchemaIn

router = APIRouter(prefix='/userlimit', tags=['UserLimitLimit'])


@router.get("", response_model=UserLimitListResponse)
def get_user_limit(user_id: Optional[str], search: str = Query(None)):
    try:
        user_limit_limits = get_user_limits(user_id, search)
        count = get_user_limit_count(user_id, search)
        return UserLimitListResponse.parse_obj({
                'result': user_limit_limits,
                'meta': {
                    'count': count
                }
            })
    except:
        raise HTTPException(404, 'User Limit Not found')


@router.post("", response_model=UserLimitResponse)
def post_user_limit(data: UserLimitSchemaIn):
    user_limit = add_user_limit(data)
    return UserLimitResponse(result=user_limit)


@router.patch("", response_model=UserLimitResponse)
def patch_user(id: str, data: UserlimitSchemaUpdateIn):
    exist_user_limit = UserLimit.get(id)
    res = update_user_limit(exist_user_limit, data)
    return UserLimitResponse(result=res)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    exist_user = UserLimit.get(id)
    db.session.delete(exist_user)
    db.session.commit()
    return






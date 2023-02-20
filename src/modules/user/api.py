from fastapi import APIRouter, Query
from fastapi_sqlalchemy import db
from starlette import status

from src.modules.user.helpers import get_users, get_user_count, add_user, update_user
from src.modules.user.model import User
from src.modules.user.schema import UserListResponse, UserResponse, UserSchemaIn, UserSchemaUpdateIn

router = APIRouter(prefix='/user', tags=['User'])


@router.get("", response_model=UserListResponse)
def get_user(search: str = Query(None)):
    users = get_users(search)
    count = get_user_count(search)
    return UserListResponse.parse_obj({
            'result': users,
            'meta': {
                'count': count
            }
        })


@router.post("", response_model=UserResponse)
def post_user(data: UserSchemaIn):
    user = add_user(data)
    return UserResponse(result=user)


@router.patch("", response_model=UserResponse)
def patch_user(id: str, data: UserSchemaUpdateIn):
    exist_user = User.get(id)
    user = update_user(exist_user, data)
    return UserResponse(result=user)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    exist_user = User.get(id)
    db.session.delete(exist_user)
    db.session.commit()
    return



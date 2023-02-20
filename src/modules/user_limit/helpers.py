from fastapi import HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.sql import or_

from src.modules.master_limit.model import MLimit
from src.modules.user_limit.model import UserLimit
from src.modules.user_limit.schema import UserLimitSchemaIn, UserLimitSchema, UserlimitSchemaUpdateIn


def get_user_limit_by_id(id):
    user_limit = db.session.get(UserLimit, id)
    if not user_limit:
        raise HTTPException(404, 'User Limit Not found')
    return user_limit


def get_user_limit_query(user_id, search=None):
    filters = []
    if user_id:
        filters.append(UserLimit.user_id == user_id)
    if search:
        filters.append(
            or_(
                UserLimit.limit_duration.ilike(f'%{search}%'),
            ))
    query = db.session.query(UserLimit).filter(*filters)
    return query


def get_user_limit_count(user_id, search=None):
    query = get_user_limit_query(user_id, search)
    return query.count()


def get_user_limits(user_id=None, search=None):
    query = get_user_limit_query(user_id, search)
    return query.all()


def add_user_limit(data: UserLimitSchemaIn) -> UserLimitSchema:
    mlimit: MLimit = MLimit.get(data.limit_id)
    user_limit = UserLimit(
        **data.dict()
    )
    user_limit.limit_duration = f"{mlimit.limit_duration} {mlimit.duration_type}"
    db.session.add(user_limit)
    db.session.commit()

    return UserLimitSchema.from_orm(user_limit)


def update_user_limit(user_limit: UserLimit, data: UserlimitSchemaUpdateIn) -> UserLimitSchema:
    values = data.dict()
    mlimit: MLimit = MLimit.get(data.limit_id)
    for key in values:
        if values[key]:
            setattr(user_limit, key, values[key])
    user_limit.limit_duration = f"{mlimit.limit_duration} {mlimit.duration_type}"
    db.session.commit()
    return UserLimitSchema.from_orm(user_limit)

from fastapi import HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.sql import or_

from src.modules.user.model import User
from src.modules.user.schema import UserSchemaIn, UserSchema, UserSchemaUpdateIn


def get_user_by_id(id):
    user = db.session.get(User, id)
    if not user:
        raise HTTPException(404, 'User Not found')
    return user


def get_user_query(search=None):
    filters = []
    if search:
        filters.append(
            or_(
                User.name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.identity_id.ilike(f'%{search}%'),
            ))
    query = db.session.query(User).filter(*filters)
    return query


def get_user_count(search=None):
    query = get_user_query(search)
    return query.count()


def get_users(search=None):
    query = get_user_query(search)
    return query.all()


def add_user(data: UserSchemaIn) -> UserSchema:
    user = User(
        **data.dict()
    )
    db.session.add(user)
    db.session.commit()

    return UserSchema.from_orm(user)


def update_user(user: User, data: UserSchemaUpdateIn) -> UserSchema:
    values = data.dict()
    for key in values:
        if values[key]:
            setattr(user, key, values[key])
    db.session.commit()
    return UserSchema.from_orm(user)

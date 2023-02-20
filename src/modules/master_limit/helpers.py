from fastapi import HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.sql import or_

from src.modules.master_limit.model import MLimit
from src.modules.master_limit.schema import MLimitSchemaIn, MLimitSchema, MLimitSchemaUpdateIn


def get_mlimit_by_id(id):
    mlimit = db.session.get(MLimit, id)
    if not mlimit:
        raise HTTPException(404, 'MLimit Not found')
    return mlimit


def get_mlimit_query(search=None):
    filters = []
    if search:
        filters.append(
            or_(
                MLimit.duration_type.ilike(f'%{search}%'),
                MLimit.limit_duration.ilike(f'%{search}%')
            ))
    query = db.session.query(MLimit).filter(*filters)
    return query


def get_mlimit_count(search=None):
    query = get_mlimit_query(search)
    return query.count()


def get_mlimits(search=None):
    query = get_mlimit_query(search)
    return query.all()


def add_mlimit(data: MLimitSchemaIn) -> MLimitSchema:
    mlimit = MLimit(
        **data.dict()
    )
    db.session.add(mlimit)
    db.session.commit()

    return MLimitSchema.from_orm(mlimit)


def update_mlimit(mlimit: MLimit, data: MLimitSchemaUpdateIn) -> MLimitSchema:
    values = data.dict()
    for key in values:
        if values[key]:
            setattr(mlimit, key, values[key])
    db.session.commit()
    return MLimitSchema.from_orm(mlimit)

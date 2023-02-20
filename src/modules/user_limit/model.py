import uuid
from typing import Union, Optional
from fastapi_sqlalchemy import db
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base


class UserLimit(Base):
    __tablename__ = 'user_limit'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))

    limit_id = Column(UUID(as_uuid=True), ForeignKey('m_limit.id'))
    limit_duration = Column(String, default=None)

    limit_total = Column(Integer, default=0)
    limit_balance = Column(Integer, default=0)
    outstanding_balance = Column(Integer, default=0)

    createdat = Column(DateTime(timezone=True), server_default=func.now())
    updatedat = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def get(cls, user_limit_id: Union[str, uuid.UUID]) -> Optional['UserLimit']:
        return db.session.get(UserLimit, user_limit_id)

    @classmethod
    def get_by_user(cls, user_id: Union[str, uuid.UUID]) -> Optional['UserLimit']:
        return db.session.query(cls).filter(cls.user_id == user_id).all()

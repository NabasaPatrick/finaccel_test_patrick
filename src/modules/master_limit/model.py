import uuid
from typing import Union, Optional
from fastapi_sqlalchemy import db
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base


class MLimit(Base):
    __tablename__ = 'm_limit'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    limit_duration = Column(String)
    duration_type = Column(String)

    createdat = Column(DateTime(timezone=True), server_default=func.now())
    updatedat = Column(DateTime(timezone=True), onupdate=func.now())


    @classmethod
    def get(cls, id) -> 'MLimit':
        return db.session.get(cls, id)

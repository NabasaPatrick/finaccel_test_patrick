import uuid
from typing import Union, Optional
from fastapi_sqlalchemy import db
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base


class Payment(Base):
    __tablename__ = 'payment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id = Column(UUID(as_uuid=True), ForeignKey('loan.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    amount = Column(Integer, default=0)
    createdat = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def get(cls, id) -> 'Payment':
        return db.session.get(cls, id)

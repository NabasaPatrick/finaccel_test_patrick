import uuid
from typing import Union, Optional
from fastapi_sqlalchemy import db
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base


class Loan(Base):
    __tablename__ = 'loan'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_limit = Column(UUID(as_uuid=True), ForeignKey('user_limit.id'))

    start_date = Column(DateTime(timezone=True))
    est_end_date = Column(DateTime(timezone=True))
    next_payment_date = Column(DateTime(timezone=True))
    last_payment_date = Column(DateTime(timezone=True))

    loan_tenur = Column(Integer, default=0)

    total_loan = Column(Integer, default=0)
    total_paid = Column(Integer, default=0)
    emi_amt = Column(Integer, default=0)

    status = Column(String, default="")

    createdat = Column(DateTime(timezone=True), server_default=func.now())
    updatedat = Column(DateTime(timezone=True), onupdate=func.now())


    @classmethod
    def get(cls, id) -> 'Loan':
        return db.session.get(cls, id)

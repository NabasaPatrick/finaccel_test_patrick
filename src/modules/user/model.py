import uuid
from typing import Union, Optional
from fastapi_sqlalchemy import db
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)
    email = Column(String, unique=True)
    identity_id = Column(String)

    createdat = Column(DateTime(timezone=True), server_default=func.now())
    updatedat = Column(DateTime(timezone=True), onupdate=func.now())


    @classmethod
    def get(cls, user_id: Union[str, uuid.UUID]) -> Optional['User']:
        return db.session.get(User, user_id)

    @classmethod
    def get_by_email(cls, email) -> Optional['User']:
        return db.session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_identity(cls, identity_id) -> Optional['User']:
        return db.session.query(cls).filter(cls.identity_id == identity_id).first()

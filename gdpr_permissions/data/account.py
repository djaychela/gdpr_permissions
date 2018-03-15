import datetime
import uuid
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-',''))
    email = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String)
    created = Column(Date, default=datetime.datetime.now)
    email_confirmed = Column(Boolean, nullable=False, default=False)
    is_super_user = Column(Boolean, nullable=False, default=False)

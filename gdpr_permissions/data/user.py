import datetime
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-',''))
    username = Column(String, unique=True)
    email = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String)
    created = Column(Date, default=datetime.datetime.now)
    cap_view = Column(Boolean, nullable=False, default=False)
    cap_edit = Column(Boolean, nullable=False, default=False)

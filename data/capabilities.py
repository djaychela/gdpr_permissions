from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Capabilities(Base):
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True)
    capability = Column(String, unique=True)
    capability_nice = Column(String, unique=True)
    active = Column(Boolean)
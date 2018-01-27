from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Classes(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    class_strand = Column(String)
    class_year = Column(String)
    class_teacher = Column(String)

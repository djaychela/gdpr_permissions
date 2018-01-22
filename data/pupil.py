from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pupils(Base):
    __tablename__ = 'pupils'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    other_names = Column(String)
    class_id = Column(Integer)
    cap_web_photo = Column(Boolean)
    cap_web_video = Column(Boolean)
    cap_ext_photo = Column(Boolean)
    cap_ext_video = Column(Boolean)
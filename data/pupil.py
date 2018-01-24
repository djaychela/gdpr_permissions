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
    damers_web = Column(Boolean, default=False)
    damers_blog = Column(Boolean, default=False)
    damers_twitter = Column(Boolean, default=False)
    damers_class_photo = Column(Boolean, default=False)
    damers_prod_dvd = Column(Boolean, default=False)
    damers_newsletter = Column(Boolean, default=False)
    wistia_video = Column(Boolean, default=False)
    dasp_web = Column(Boolean, default=False)
    dasp_music_web = Column(Boolean, default=False)
    dor_echo = Column(Boolean, default=False)
    cel_pound_mag = Column(Boolean, default=False)
    cel_pound_web = Column(Boolean, default=False)


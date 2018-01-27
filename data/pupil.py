from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from gdpr_permissions.data.classes import Classes

Base = declarative_base()


class Classes(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    class_strand = Column(String)
    class_year = Column(String)
    class_teacher = Column(String)

class Pupils(Base):
    __tablename__ = 'pupils'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    other_names = Column(String)
    class_id = Column(Integer, ForeignKey('classes.id'))
    class_info = relationship('Classes')
    overview = Column(Enum('ok','check','none'))
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


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
    c1 = Column(Boolean, default=False)
    c2 = Column(Boolean, default=False)
    c3 = Column(Boolean, default=False)
    c4 = Column(Boolean, default=False)
    c5 = Column(Boolean, default=False)
    c6 = Column(Boolean, default=False)
    c7 = Column(Boolean, default=False)
    c8 = Column(Boolean, default=False)
    c9 = Column(Boolean, default=False)
    c10 = Column(Boolean, default=False)
    c11 = Column(Boolean, default=False)
    c12 = Column(Boolean, default=False)
    c13 = Column(Boolean, default=False)
    c14 = Column(Boolean, default=False)
    c15 = Column(Boolean, default=False)
    c16 = Column(Boolean, default=False)
    c17 = Column(Boolean, default=False)
    c18 = Column(Boolean, default=False)
    c19 = Column(Boolean, default=False)
    c20 = Column(Boolean, default=False)
    c21 = Column(Boolean, default=False)
    c22 = Column(Boolean, default=False)
    c23 = Column(Boolean, default=False)
    c24 = Column(Boolean, default=False)
    c25 = Column(Boolean, default=False)
    c26 = Column(Boolean, default=False)
    c27 = Column(Boolean, default=False)
    c28 = Column(Boolean, default=False)
    c29 = Column(Boolean, default=False)
    c30 = Column(Boolean, default=False)



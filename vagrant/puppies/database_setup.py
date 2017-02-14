"""
Setup database
"""
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    shelter_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zip_code = Column(String(250), nullable=False)
    website = Column(String(250), nullable=False)


class Puppy(Base):
    __tablename__ = 'puppy' # Table information
    puppy_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date_of_birth = Column(Date(), nullable=False)
    gender = Column(String(6), nullable=False)
    weight = Column(Float(), nullable=False)
    picture = Column(String(250), nullable=False)
    shelter_id = Column(Integer, ForeignKey('shelter.shelter_id'))
    shelter = relationship(Shelter)



engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)

"""
Setup database
"""
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zip_code = Column(String(250), nullable=False)
    website = Column(String(250))
    shelter_id = Column(Integer, primary_key=True)


class Puppy(Base):
    __tablename__ = 'puppy' # Table information
    name = Column(String(250), nullable=False)
    date_of_birth = Column(Date())
    gender = Column(Boolean(), nullable=False)
    weight = Column(Float())
    picture = Column(String(250))
    shelter_id = Column(Integer, ForeignKey('shelter.shelter_id'))
    shelter = relationship(Shelter)



engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Query all puppies by ascending weight
for puppy in session.query(Puppy).order_by(Puppy.weight):
    print("name:{:>9}, weight:{:>14}, shelter:{:>2}".\
        format(puppy.name, puppy.weight, puppy.shelter_id))

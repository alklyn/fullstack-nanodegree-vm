from sqlalchemy import create_engine, func
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

# Query all puppies grouped by the shelter in which they are staying
result = session.query(Shelter, func.count(Puppy.puppy_id))\
    .join(Puppy).group_by(Shelter.shelter_id).all()

for item in result:
    print("shelter_id:{:>4}, Shelter name:{:>50}, Number of puppies:{:>4} "\
        .format(item[0].shelter_id, item[0].name, item[1]))

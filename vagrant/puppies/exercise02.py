from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from database_setup import Base, Shelter, Puppy
import datetime


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Query all of the puppies that are less than 6 months old organized by the
# youngest first.

today = datetime.date.today()
td = datetime.timedelta(days=180) # Assume each month is 30days
cutoff = today - td # Calculate a date where the age is 180days
q_obj = session.query(Puppy).order_by(desc(Puppy.date_of_birth))\
    .filter(Puppy.date_of_birth > cutoff)


for puppy in q_obj:
    age_td = today - puppy.date_of_birth
    age = age_td.days
    print("Name: {}, DOB: {}, Age: {} days"
        .format(puppy.name, puppy.date_of_birth, age))

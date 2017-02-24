from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_restaurant(name):
    """
    Add a new restaurant to the database
    """
    new_restaurant = Restaurant(name=name)
    session.add(new_restaurant)
    session.commit()
    print("Restaurant added to database.")

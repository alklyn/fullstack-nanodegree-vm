from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_restaurants():
    """
    Get a list of all the restaurants in the database.
    """
    results = session.query(Restaurant).order_by(Restaurant.name)
    for item in results:
        print("id:{:>2}, name:{:>40}".format(item.id, item.name))
    return results


get_restaurants()

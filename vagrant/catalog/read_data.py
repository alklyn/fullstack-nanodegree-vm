from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurants = session.query(Restaurant).all()

for restaurant in restaurants:
    print("id: {}, name: {}".format(restaurant.restaurant_id, restaurant.name))

menu_items = session.query(MenuItem).all()

for menu_item in menu_items:
    print("restaurant_id: {}, id: {}, name: {}, description: {}, course: {}, price: {}"\
    .format(menu_item.restaurant_id, menu_item.menu_id, menu_item.name, menu_item.description, menu_item.course, menu_item.price))

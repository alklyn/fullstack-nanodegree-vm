from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from my_html import base, menu_content, menu_item

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) # Create an instance of the Flask class

@app.route("/")
@app.route("/menu_items")
def Menu():
    """
    Display menu
    """
    restaurant = session.query(Restaurant).first() # Get the first restaurant
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    menu_list =""
    for item in menu:
        menu_list += menu_item.format(
            name=item.name,
            price=item.price,
            description=item.description)

    content = menu_content.format(
        restaurant_name=restaurant.name,
        menu_list=menu_list)
        
    output = base.format(title=restaurant.name, content=content)
    return output

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True, host="0.0.0.0", port=8080)

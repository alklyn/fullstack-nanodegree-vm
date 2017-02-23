from flask import Flask, render_template, url_for, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from my_html import base, menu_content, menu_item

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) # Create an instance of the Flask class

@app.route("/")
@app.route("/restaurants/")
def restaurants():
    """
    Display restaurants
    """
    restaurants = session.query(Restaurant).order_by(Restaurant.id)
    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/restaurants/<int:restaurant_id>/")
def menu(restaurant_id=-1):
    """
    Display menu
    """
    if restaurant_id == -1:
        restaurant = \
            session.query(Restaurant).order_by(Restaurant.id.desc()).first()
    elif restaurant_id == 0:
        restaurant = session.query(Restaurant).first()
    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).first()

    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template(
        "menu.html",
        restaurant=restaurant,
        menu=menu)


# Task 1: Create route for newMenuItem function here
@app.route(
    "/restaurants/new_menu_item/<int:restaurant_id>/",
    methods=["GET", "POST"])
def new_menu_item(restaurant_id):
    if request.method == "POST":
        if request.form["choice"] == "create":
            new_item = MenuItem(
                name=request.form["name"],
                description=request.form["description"],
                price="$" + request.form["price"],
                course=request.form["course"],
                restaurant_id=restaurant_id)

            session.add(new_item)
            session.commit()
        # Display the newly created menu item
        return redirect(url_for('menu', restaurant_id=restaurant_id))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template("new_menu_item.html", restaurant=restaurant)


# Task 2: Create route for editMenuItem function here
@app.route(
    "/restaurants/edit_menu_item/<int:restaurant_id>/<int:menu_id>/",
    methods=["GET", "POST"])
def edit_menu_item(restaurant_id, menu_id):
    if request.method == "POST":
        if request.form["choice"] == "edit":
            menu_item = \
                session.query(MenuItem).filter_by(id=menu_id).first()

            menu_item.name = request.form["name"]
            menu_item.description = request.form["description"]
            menu_item.price = request.form["price"]
            menu_item.course = request.form["course"]

            session.add(menu_item)
            session.commit()
        # Display the newly edited menu item
        return redirect(url_for('menu', restaurant_id=restaurant_id))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).first()
        menu_item = \
            session.query(MenuItem).filter_by(id=menu_id).first()

        return render_template(
            "edit_menu_item.html",
            restaurant=restaurant,
            menu_item=menu_item)

# Task 3: Create a route for deleteMenuItem function here
@app.route(
    "/restaurants/delete_menu_item/<int:restaurant_id>/<int:menu_id>/",
    methods=["GET", "POST"])
def delete_menu_item(restaurant_id, menu_id):
    if request.method == "POST":
        if request.form["choice"] == "delete":
            menu_item = \
                session.query(MenuItem).filter_by(id=menu_id).first()

            session.delete(menu_item)
            session.commit()
        # Display list of menu items
        return redirect(url_for('menu', restaurant_id=restaurant_id))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).first()
        menu_item = \
            session.query(MenuItem).filter_by(id=menu_id).first()

        return render_template(
            "delete_menu_item.html",
            restaurant=restaurant,
            menu_item=menu_item)

if __name__ == "__main__":
    app.secret_key = "Ut0ndr1agr14*$hitmh@7ayAk0*"
    app.debug = True
    app.run(debug=True, host="0.0.0.0", port=8080)

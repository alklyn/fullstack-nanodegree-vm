from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import fake_db

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) # Create an instance of the Flask class

courses = [
    "Appetizer",
    "Entree",
    "Dessert",
    "Beverage"
]

# Making an API Endpoint (GET Request)
@app.route("/restaurants/<int:restaurant_id>/menu/JSON")
def restaurant_menu_json(restaurant_id):
    """
    JSON API Endpoint
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = \
        session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(menu=[item.serialize for item in menu_items])


# Making an API Endpoint (GET Request)
@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def menu_item_json(restaurant_id, menu_id):
    """
    JSON API Endpoint
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menu_item=menu_item.serialize)


@app.route("/")
@app.route("/restaurants/")
def restaurants():
    """
    Display restaurants
    """
    restaurants = session.query(Restaurant).order_by(Restaurant.id).all()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/restaurants/new_restaurant/")
def new_restaurant():
    """
    Add a new restaurant.
    """
    return render_template("new_restaurant.html")


@app.route("/restaurants/edit_restaurant/<int:restaurant_id>/")
def edit_restaurant(restaurant_id):
    """
    Edit restaurant details.
    """
    restaurant = fake_db.restaurant
    return render_template("edit_restaurant.html", restaurant=restaurant)


@app.route("/restaurants/delete_restaurant/<int:restaurant_id>/")
def delete_restaurant(restaurant_id):
    """
    Delete restaurant.
    """
    restaurant = fake_db.restaurant
    return render_template("delete_restaurant.html", restaurant=restaurant)


@app.route("/restaurants/<int:restaurant_id>/")
@app.route("/restaurants/<int:restaurant_id>/show_menu")
def show_menu(restaurant_id=-1):
    """
    Display menu for the selected restaurant.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template("menu.html", restaurant=restaurant, menu=menu)


@app.route(
    "/restaurants/new_menu_item/<int:restaurant_id>/", methods=["GET", "POST"])
def new_menu_item(restaurant_id):
    """
    Create a new menu item for the selected restaurant.
    """
    if request.method == "POST":
        if request.form["choice"] == "create":
            new_item = MenuItem(
                name=request.form["name"],
                description=request.form["description"],
                price=request.form["price"],
                course=request.form["course"],
                restaurant_id=restaurant_id)

            session.add(new_item)
            session.commit()
            flash("New menu item created.")
        # Display the newly created menu item
        return redirect(url_for('menu', restaurant_id=restaurant_id))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template(
            "new_menu_item.html",
            restaurant=restaurant,
            courses=courses)


@app.route(
    "/restaurants/edit_menu_item/<int:restaurant_id>/<int:menu_id>/",
    methods=["GET", "POST"])
def edit_menu_item(restaurant_id, menu_id):
    """
    Edit selected menu item.
    """
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
            flash("Menu item edited.")
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
            menu_item=menu_item,
            courses=courses)


@app.route(
    "/restaurants/delete_menu_item/<int:restaurant_id>/<int:menu_id>/",
    methods=["GET", "POST"])
def delete_menu_item(restaurant_id, menu_id):
    """
    Delete the selected menu item.
    """
    return "This page will delete menu item {}.".format(menu_id)


if __name__ == "__main__":
    app.secret_key = "Ut0ndr1agr14*$hi7mh@7ayAk0*"
    app.debug = True
    app.run(debug=True, host="0.0.0.0", port=8080)

from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
from flask import session as login_session
from flask import make_response

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User


engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) # Create an instance of the Flask class

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

courses = [
    "Appetizer",
    "Entree",
    "Dessert",
    "Beverage"
]


@app.route("/login/")
def show_login():
    """
    Create a state token to prevent request forgery.
    Store it in the session for later validation.
    """
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session["state"] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create a new user if the user is not already in the database
    print("email = {}".format(login_session['email']))
    login_session['user_id'] = get_user_id(login_session['email'])
    print("User id = {}".format(get_user_id(login_session['email'])))
    if login_session['user_id'] is None:
        login_session['user_id'] = create_user(login_session)


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect/')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	del login_session['user_id']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:

    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


@app.route("/restaurants/JSON/")
def restaurants_json():
    """
    JSON API to view restaurants.
    """
    restaurants = session.query(Restaurant).all()
    return jsonify(menu=[restaurant.serialize for restaurant in restaurants])


@app.route("/restaurants/<int:restaurant_id>/menu/JSON/")
def restaurant_menu_json(restaurant_id):
    """
    JSON APIs to view a restaurant's menu.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = \
        session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(menu=[item.serialize for item in menu_items])


@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/")
def menu_item_json(restaurant_id, menu_id):
    """
    JSON APIs to view a menu item.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menu_item=menu_item.serialize)


@app.route("/")
@app.route("/restaurants/")
def restaurants():
    """
    Display restaurants.
    Only the owner of a restaurant has the options to edit or view it.
    """
    restaurants = session.query(Restaurant).order_by(Restaurant.id).all()

    if "user_id" not in login_session:
        return render_template(
            "restaurants.html",
            restaurants=restaurants,
            current_user_id=None)
    else:
        current_user_id = login_session["user_id"]
        print("current_user_id: {}".format(current_user_id))
        return render_template(
            "restaurants.html",
            restaurants=restaurants,
            current_user_id=current_user_id)


@app.route("/restaurants/new_restaurant/", methods=["GET", "POST"])
def new_restaurant():
    """
    Add a new restaurant.
    """
    if "username" not in login_session:
        return redirect("/login/")

    if request.method == "POST":
        if request.form["choice"] == "create":
            user_id = login_session["user_id"]
            restaurant = Restaurant(name=request.form["name"], user_id=user_id)
            session.add(restaurant)
            session.commit()

            flash("New Restaurant Created.")
        return redirect(url_for('restaurants'))
    else:
        return render_template("new_restaurant.html")


@app.route(
    "/restaurants/edit_restaurant/<int:restaurant_id>/",
    methods=["GET", "POST"])
def edit_restaurant(restaurant_id):
    """
    Edit restaurant details.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if "username" not in login_session:
        return redirect("/login/")
    elif login_session["user_id"] != restaurant.user_id:
        flash("Only the owner can edit a restaurant.")
        return redirect(url_for('restaurants'))

    if request.method == "POST":
        if request.form["choice"] == "edit":
            restaurant.name = request.form["name"]
            session.add(restaurant)
            session.commit()

            flash("Restaurant Successfully Edited.")
        return redirect(url_for('restaurants'))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template("edit_restaurant.html", restaurant=restaurant)


@app.route(
    "/restaurants/delete_restaurant/<int:restaurant_id>/",
    methods=["GET", "POST"])
def delete_restaurant(restaurant_id):
    """
    Delete restaurant.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if "username" not in login_session:
        return redirect("/login/")
    elif login_session["user_id"] != restaurant.user_id:
        flash("Only the owner can delete a restaurant.")
        return redirect(url_for('restaurants'))

    if request.method == "POST":
        if request.form["choice"] == "delete":
            restaurant = \
                session.query(Restaurant).filter_by(id=restaurant_id).one()
            session.delete(restaurant)
            session.commit()

            flash("Restaurant Successfully Deleted.")
        return redirect(url_for('restaurants'))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template("delete_restaurant.html", restaurant=restaurant)


@app.route("/restaurants/<int:restaurant_id>/")
@app.route("/restaurants/<int:restaurant_id>/show_menu/")
def show_menu(restaurant_id=-1):
    """
    Display menu for the selected restaurant.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    menus = list()
    for course in courses:
        # Make separate queries for each course
        print("course: {}".format(course))
        menus.append(session.query(MenuItem)\
            .filter(and_(MenuItem.restaurant_id == restaurant.id,
            MenuItem.course == course))\
            .order_by(MenuItem.course, MenuItem.name))

    return render_template(
        "menu.html",
        restaurant=restaurant,
        menus=menus,
        courses=courses)


@app.route(
    "/restaurants/new_menu_item/<int:restaurant_id>/", methods=["GET", "POST"])
def new_menu_item(restaurant_id):
    """
    Create a new menu item for the selected restaurant.
    """
    if "username" not in login_session:
        return redirect("/login/")

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if request.method == "POST":
        if request.form["choice"] == "create":
            new_item = MenuItem(
                name=request.form["name"],
                description=request.form["description"],
                price=request.form["price"],
                course=request.form["course"],
                restaurant_id=restaurant_id,
                user_id=restaurant.user_id
                )

            session.add(new_item)
            session.commit()
            flash("New Menu Item '{}' Created.".format(new_item.name))
        # Display the newly created menu item
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))

    else:
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
    if "username" not in login_session:
        return redirect("/login/")

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
            flash("Menu Item Successfully Edited.")
        # Display the newly edited menu item
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))

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
    if "username" not in login_session:
        return redirect("/login/")

    if request.method == "POST":
        if request.form["choice"] == "delete":
            menu_item = \
                session.query(MenuItem).filter_by(id=menu_id).first()

            session.delete(menu_item)
            session.commit()
            flash("Menu Item Successfully Deleted.")
        # Display list of menu items
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))

    else:
        restaurant = \
            session.query(Restaurant).filter_by(id=restaurant_id).first()
        menu_item = \
            session.query(MenuItem).filter_by(id=menu_id).first()

        return render_template(
            "delete_menu_item.html",
            restaurant=restaurant,
            menu_item=menu_item)


def create_user(login_session):
    new_user = User(
        name=login_session["username"],
        email=login_session["email"],
        picture=login_session["picture"])
    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(email=login_session["email"]).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == "__main__":
    app.secret_key = "Ut0ndr1agr14*$hi7mh@7ayAk0*"
    app.debug = True
    app.run(debug=True, host="0.0.0.0", port=8080)

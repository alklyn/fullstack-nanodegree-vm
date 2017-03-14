from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
from flask import session
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
from database_setup import Base, ISP, Package, User

engine = create_engine("sqlite:///isp.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask(__name__)
user_id = 1


@app.route("/")
@app.route("/isps/")
def show_isps():
    """
    This page will show a list of all the ISPs in the database.
    """
    isps = db_session.query(ISP).order_by(ISP.name)
    return render_template("isps.html", isps=isps)


@app.route("/isp/new/", methods=["GET", "POST"])
def new_isp():
    """
    This page will be for adding a new ISP to the database.
    """
    if request.method == "POST":
        if request.form["choice"] == "create":
            isp = ISP(name=request.form["name"], user_id=user_id)
            db_session.add(isp)
            db_session.commit()
            flash("New ISP Successfully Created.")
        return redirect(url_for('show_isps'))
    else:
        return render_template("new_isp.html")


@app.route("/isps/<int:isp_id>/edit/", methods=["GET", "POST"])
def edit_isp(isp_id):
    """
    This page will be for editing ISPs in the database.
    """
    isp = db_session.query(ISP).filter_by(id=isp_id).one()
    if request.method == "POST":
        if request.form["choice"] == "edit":
            isp.name = request.form["name"]
            db_session.add(isp)
            db_session.commit()
            flash("ISP Successfully Edited.")
        return redirect(url_for('show_isps'))
    else:
        return render_template("edit_isp.html", isp=isp)


@app.route("/isps/<int:isp_id>/delete/", methods=["GET", "POST"])
def delete_isp(isp_id):
    """
    This page will be for deleting ISPs in the database.
    """
    isp = db_session.query(ISP).filter_by(id=isp_id).one()
    if request.method == "POST":
        if request.form["choice"] == "delete":
            db_session.delete(isp)
            db_session.commit()
            flash("ISP Successfully Deleted.")
        return redirect(url_for('show_isps'))
    else:
        return render_template("delete_isp.html", isp=isp)


@app.route("/isps/<int:isp_id>/")
@app.route("/isps/<int:isp_id>/packages/")
def show_packages(isp_id):
    """
    This page will show a list of all the packages offered by the ISP.
    """
    isp = db_session.query(ISP).filter_by(id=isp_id).one()
    packages = db_session.query(Package).filter_by(isp_id=isp_id)\
        .order_by(Package.name)
    return render_template("packages.html", isp=isp, packages=packages)


@app.route("/isps/<int:isp_id>/new_package/", methods=["GET", "POST"])
def new_package(isp_id):
    """
    This page will add a new package to the ISP identified by isp_id.
    """
    isp = db_session.query(ISP).filter_by(id=isp_id).one()
    if request.method == "POST":
        if request.form["choice"] == "create":
            package = Package(
                name=request.form["name"],
                bandwidth=int(request.form["bandwidth"]),
                cap=int(request.form["cap"]),
                price=float(request.form["price"]),
                user_id=user_id,
                isp_id=isp_id)
            db_session.add(package)
            db_session.commit()
            flash("New Package Successfully Created.")

        return redirect(url_for('show_packages', isp_id=isp_id))
    else:
        return render_template("new_package.html", isp=isp)


@app.route(
    "/isps/<int:isp_id>/packages/<int:package_id>/edit/",
    methods=["GET", "POST"])
def edit_package(isp_id, package_id):
    """
    This page will be for editing packages in the database.
    """
    isp = db_session.query(ISP).filter_by(id=isp_id).one()
    package = db_session.query(Package).filter_by(id=package_id).one()

    if request.method == "POST":
        if request.form["choice"] == "edit":
            package.name = request.form["name"]
            package.bandwidth = int(request.form["bandwidth"])
            package.cap = int(request.form["cap"])
            package.price = float(request.form["price"])
            db_session.add(package)
            db_session.commit()
            flash("Package Updated.")

        return redirect(url_for('show_packages', isp_id=isp_id))
    else:
        return render_template("edit_package.html", isp=isp, package=package)


@app.route(
    "/isps/<int:isp_id>/packages/<int:package_id>/delete/",
    methods=["GET", "POST"])
def delete_package(isp_id, package_id):
    """
    This page will be for deleting packages in the database.
    """
    isp = db_session.query(ISP).filter_by(id=isp_id).one()
    package = db_session.query(Package).filter_by(id=package_id).one()

    if request.method == "POST":
        if request.form["choice"] == "delete":
            db_session.delete(package)
            db_session.commit()
            flash("Package Updated.")

        return redirect(url_for('show_packages', isp_id=isp_id))
    else:
        return render_template("delete_package.html", isp=isp, package=package)


if __name__ == "__main__":
    app.secret_key = "Ut0ndr1agr14*$hi7mh@7ayAk0*"
    app.debug = True
    app.run(host="0.0.0.0", port=8080)

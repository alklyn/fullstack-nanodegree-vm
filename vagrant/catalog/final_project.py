from flask import Flask
from fake_db import isps, packages

app = Flask(__name__)


@app.route("/")
@app.route("/isp/")
def isp():
    """
    This page will show a list of all the ISPs in the database.
    """
    return ("This page will show a list of all the ISPs.")


@app.route("/isp/new/", methods=["GET", "POST"])
def new_isp():
    """
    This page will be for adding a new ISP to the database.
    """
    return ("This page will be for adding a new isp to the database.")


@app.route("/isp/<int:isp_id>/edit/", methods=["GET", "POST"])
def edit_isp(isp_id):
    """
    This page will be for editing ISPs in the database.
    """
    return (
        "This page will be for editing ISP {} in the database.".format(isp_id))


@app.route("/isp/<int:isp_id>/delete/", methods=["GET", "POST"])
def delete_isp(isp_id):
    """
    This page will be for deleting ISPs in the database.
    """
    return ("Form to delete ISP {} in the database."
            .format(isp_id))


@app.route("/isp/<int:isp_id>/", methods=["GET", "POST"])
@app.route("/isp/<int:isp_id>/packages/", methods=["GET", "POST"])
def show_packages(isp_id):
    """
    This page will show a list of all the packages offered by the ISP.
    """
    return ("This page will show this ISP's packages.")


@app.route(
    "/isp/<int:isp_id>/packages/<int:package_id>/edit/",
    methods=["GET", "POST"])
def edit_package(isp_id, package_id):
    """
    This page will be for editing packages in the database.
    """
    return ("This page will be for editing packages in the database.")


@app.route(
    "/isp/<int:isp_id>/packages/<int:package_id>/delete/",
    methods=["GET", "POST"])
def edit_package(isp_id, package_id):
    """
    This page will be for deleting packages in the database.
    """
    return ("This page will be for deleting packages in the database.")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)

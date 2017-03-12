from flask import Flask, render_template
from fake_db import isps, packages

app = Flask(__name__)


@app.route("/")
@app.route("/isp/")
def isp():
    """
    This page will show a list of all the ISPs in the database.
    """
    return render_template("isps.html", isps=isps)


@app.route("/isp/new/", methods=["GET", "POST"])
def new_isp():
    """
    This page will be for adding a new ISP to the database.
    """
    return render_template("new_isp.html")


@app.route("/isp/<int:isp_id>/edit/", methods=["GET", "POST"])
def edit_isp(isp_id):
    """
    This page will be for editing ISPs in the database.
    """
    isp = isps[isp_id - 1]
    return render_template("edit_isp.html", isp=isp)


@app.route("/isp/<int:isp_id>/delete/", methods=["GET", "POST"])
def delete_isp(isp_id):
    """
    This page will be for deleting ISPs in the database.
    """
    isp = isps[isp_id - 1]
    return render_template("delete_isp.html", isp=isp)


@app.route("/isp/<int:isp_id>/")
@app.route("/isp/<int:isp_id>/packages/")
def show_packages(isp_id):
    """
    This page will show a list of all the packages offered by the ISP.
    """
    isp = isps[isp_id - 1]

    req_packages = [pac for pac in packages if pac["isp_id"] == isp_id]
    return render_template("packages.html", isp=isp, packages=req_packages)


@app.route("/isp/<int:isp_id>/new_package/", methods=["GET", "POST"])
def new_package(isp_id):
    """
    This page will show a list of all the packages offered by the ISP.
    """
    isp = isps[isp_id - 1]

    return render_template("new_package.html", isp=isp)


@app.route(
    "/isp/<int:isp_id>/packages/<int:package_id>/edit/",
    methods=["GET", "POST"])
def edit_package(isp_id, package_id):
    """
    This page will be for editing packages in the database.
    """
    isp = isps[isp_id - 1]
    for package in packages:
        if package["id"] == package_id:
            break
    return render_template("edit_package.html", isp=isp, package=package)


@app.route(
    "/isp/<int:isp_id>/packages/<int:package_id>/delete/",
    methods=["GET", "POST"])
def delete_package(isp_id, package_id):
    """
    This page will be for deleting packages in the database.
    """
    isp = isps[isp_id - 1]
    for package in packages:
        if package["id"] == package_id:
            break
    return render_template("delete_package.html", isp=isp, package=package)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)

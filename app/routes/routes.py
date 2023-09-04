from flask import Blueprint, render_template


routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/")
def index():
    return render_template("index.html", results=None, message=None)


@routes_bp.route("/admin")
def admin():
    return render_template("admin.html", results=None)


@routes_bp.route("/create_employee")
def create_employee():
    return render_template("create_employee.html")

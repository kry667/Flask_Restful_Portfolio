from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/", endpoint="index")
def index():
    return render_template("index.html", results=None, message=None)



@routes_bp.route("/admin", endpoint="admin")
@jwt_required()
def admin():
    return render_template("admin.html", results=None)
    


@routes_bp.route("/create_employee", endpoint="create_employee")
def create_employee():
    return render_template("create_employee.html")

from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/", endpoint="index")
def index():
    return render_template("index.html", results=None, message=None)

@routes_bp.route("/admin", endpoint="admin")

def admin():
    
    # # Retrieve the user data from the JWT
    # current_user = get_jwt_identity()
    
    # if current_user and current_user.get("admin"):
    #     # You can use the user data from the JWT as needed
        return render_template("admin.html", results=None)
    
    # Handle the case where the user is not an admin
    # return "Access denied: Admin access required"

@routes_bp.route("/create_employee", endpoint="create_employee")
@jwt_required()
def create_employee():
    # Retrieve the user data from the JWT
    current_user = get_jwt_identity()
    
    if current_user:
        # You can use the user data from the JWT as needed
        return render_template("create_employee.html")
    
    # Handle the case where there's no valid user in the JWT
    return "Access denied: User authentication required"

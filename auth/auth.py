import os
import requests
import uuid  # Import UUID for generating a unique token identifier

from datetime import timedelta
from functools import wraps
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from redis import Redis

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity


from flask import Flask
from flask import jsonify
from flask import request


load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)

redis_client = Redis(host="redis", port=6379)  # Use the service name from Docker Compose
app.config["JWT_BLACKLIST_STORE"] = redis_client

jwt = JWTManager(app)


@app.route("/login", methods=["GET", "POST"])
def login():

    employee_id = request.args.get("login")
    password = request.args.get("password")

    user_crud_url = f"http://employee_crud:5000/employees/{employee_id}"
    try:
        response = requests.get(user_crud_url)
        
        if response.status_code == 200:
            employee_data = response.json()

            if employee_data and employee_data[0]["id"] == int(employee_id):
                # Check if the provided password matches the hashed password
                if check_password_hash(employee_data[0]["password"], password):

                    access_token = create_access_token(identity=employee_data,
                                                       additional_claims={"admin": True})
                    # Generate a unique identifier for the token
                    token_identifier = "aaa"
                    
                    # Store the token in Redis with the identifier
                    redis_client.set(token_identifier, access_token, ex=3600)
                    print(access_token)  # Set expiration time as needed
                    return jsonify({"logged": True, "token_identifier": token_identifier})

    except Exception:
        pass

    return None


# Function to generate a unique token identifier
def generate_unique_token_identifier():
    # Use UUID to generate a unique identifier
    return str(uuid.uuid4())

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get("admin") == True:
            return function(*args, **kwargs)
        else:
            return jsonify({"message": "Admin access required"}), 403  # Forbidden

    return wrapper



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

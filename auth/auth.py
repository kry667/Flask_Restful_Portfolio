import os
import requests
import uuid

from datetime import timedelta
from functools import wraps
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from redis import Redis, ConnectionPool

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
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)

redis_pool = ConnectionPool(host="redis", port=6379, decode_responses=True)
redis_client = Redis(connection_pool=redis_pool)
app.config["JWT_BLACKLIST_STORE"] = redis_client

jwt = JWTManager(app)


@app.route("/login", methods=["GET", "POST"])
def login():

    employee_id = request.args.get("login")
    password = request.args.get("password")
    
    # Create temporary token to access the employees Resource
    temp_token = create_access_token(identity="temp")
    redis_client.set("temp", temp_token, ex=15)
    headers = {"Authorization": f"Bearer {temp_token}"}

    employee_crud_url = f"http://employee_crud:5000/employees/{employee_id}"
    try:
        response = requests.get(employee_crud_url, headers=headers)
        
        if response.status_code == 200:
            employee_data = response.json()

            # Check if the provided password matches the hashed password
            if check_password_hash(employee_data[0]["password"], password):

                access_token = create_access_token(identity=employee_data,
                                                    additional_claims={"admin": True})
                # Generate a unique identifier for the token
                token_identifier = generate_unique_token_identifier()
                
                # Store the token in Redis with the identifier
                redis_client.set(token_identifier, access_token, ex=60)
                return jsonify({"logged": True, "token_identifier": token_identifier}), 200

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

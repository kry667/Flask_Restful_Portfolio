from flask import Flask
from routes.customer_routes import customer_routes_bp 
from routes.employee_routes import employee_routes_bp
from routes.routes import routes_bp
from flask_jwt_extended import JWTManager
from redis import Redis, ConnectionPool
import os


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

app.secret_key = "your_secret_key_here"

redis_pool = ConnectionPool(host="redis", port=6379, decode_responses=True)
redis_client = Redis(connection_pool=redis_pool)
app.config["JWT_BLACKLIST_STORE"] = redis_client

jwt = JWTManager(app)


app.register_blueprint(routes_bp)
app.register_blueprint(employee_routes_bp)
app.register_blueprint(customer_routes_bp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    
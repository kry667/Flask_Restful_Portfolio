import os
from dotenv import load_dotenv
from flask import Flask, request, current_app
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from redis import Redis, ConnectionPool


if 'ENV' in os.environ and os.environ['ENV'] == 'testing':
    # Load testing environment variables from .env.testing
    load_dotenv('.env.testing')

# Load production environment variables from .env
load_dotenv()

app = Flask(__name__)
api = Api(app)

redis_pool = ConnectionPool(host="redis", port=6379, decode_responses=True)
redis_client = Redis(connection_pool=redis_pool)
app.config["JWT_BLACKLIST_STORE"] = redis_client

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"


jwt = JWTManager(app)


app.config[
    "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DB']}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    city = db.Column(db.String(100))
    street = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    state = db.Column(db.String(100))


# Define fields for marshaling
customer_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "phone": fields.String,
    "city": fields.String,
    "street": fields.String,
    "zip_code": fields.String,
    "state": fields.String,
}


class QueryResource(Resource):
    @jwt_required()
    @marshal_with(customer_fields)
    def get(self):
        search_query = request.args.get("query")

        if search_query is None:
            return {"message": "Query parameter 'query' is missing or invalid"}, 400
        
        try:
            results = self.query_customers(search_query)
            return results
        except SQLAlchemyError as e:
            # Handle the database error and return an error response
            db.session.rollback()  # Rollback the database transaction
            error_message = "Database error"
            return {"message": error_message}, 500

    def query_customers(self, search_query):
        try:
            results = Customers.query.filter(
                or_(
                    Customers.id == search_query,
                    Customers.first_name.like(f"%{search_query}%"),
                    Customers.last_name.like(f"%{search_query}%"),
                    Customers.email.like(f"%{search_query}%"),
                    Customers.phone.like(f"%{search_query}%"),
                    Customers.city.like(f"%{search_query}%"),
                )
            ).all()
            return results
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the database transaction
            error_message = "Database error"
            # Handle the database error and return an appropriate response
            return {"message": error_message}, 500



class CustomersResource(Resource):
    @jwt_required()
    @marshal_with(customer_fields)
    def get(self, customer_id=None):
        access_token = current_app.config.get("MY_GLOBAL_TOKEN")
        if customer_id is None:
            # Retrieve all customers
            results = Customers.query.all()
        else:
            # Retrieve a single customer by ID
            customer = Customers.query.get(customer_id)
            results = [customer] if customer else []

        return results


class UpdateUserResource(Resource):
    def patch(self, customer_id):
        try:
            data = request.get_json()

            customer = Customers.query.get(customer_id)
            if not customer:
                return {"message": "Customer not found"}, 404

            # Update customer fields from the JSON data
            customer.city = data.get("city", customer.city)
            customer.first_name = data.get("first_name", customer.first_name)
            customer.last_name = data.get("last_name", customer.last_name)
            customer.email = data.get("email", customer.email)
            customer.phone = data.get("phone", customer.phone)
            customer.street = data.get("street", customer.street)
            customer.zip_code = data.get("zip_code", customer.zip_code)
            customer.state = data.get("state", customer.state)

            db.session.commit()

            return {"message": "Customer updated successfully"}, 200

        except Exception as e:
            return {"message": "An error occurred while updating the customer"}, 500


class DeleteUserResource(Resource):
    def delete(self, customer_id):
        try:
            customer = Customers.query.get(customer_id)
            if not customer:
                return {"message": "Customer not found"}, 404

            db.session.delete(customer)
            db.session.commit()

            return {"message": "Customer deleted successfully"}, 200

        except Exception as e:
            return {"message": "An error occurred while deleting the customer"}, 500


api.add_resource(DeleteUserResource, "/delete_user/<int:customer_id>")
api.add_resource(UpdateUserResource, "/update_user/<int:customer_id>")
api.add_resource(CustomersResource, "/customers", "/customer_edit/<int:customer_id>")
api.add_resource(QueryResource, "/query_customers")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

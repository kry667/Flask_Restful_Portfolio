import os

from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
api = Api(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DB']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean(10))


employees_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "phone": fields.String,
    "email": fields.String,
    "password": fields.String,
    "admin": fields.Boolean,
}


class EmployeesResource(Resource):
    @marshal_with(employees_fields)
    def get(self, employee_id=None):
        if employee_id == None:
            results = Employees.query.all()
        else:
            employee = Employees.query.get(employee_id)
            results = [employee] if employee else []

        return results, 200


class QueryEmployees(Resource):
    @marshal_with(employees_fields)
    def get(self):
        search_query = request.args.get("query")
        results = self.query_employees(search_query)
        return results

    def query_employees(self, search_query):
        results = Employees.query.filter(
            or_(
                Employees.id == search_query,
                Employees.first_name.like(f"%{search_query}%"),
                Employees.last_name.like(f"%{search_query}%"),
                Employees.phone.like(f"%{search_query}%"),
                Employees.email.like(f"%{search_query}%"),
            )
        ).all()
        return results


class UpdateEmployeeResource(Resource):
    def patch(self, employee_id):
        try:
            data = request.get_json()

            employee = Employees.query.get(employee_id)
            if not employee:
                return {"message": "Customer not found"}, 404

            # Hash the password from request data, if provided
            hashed_password = None
            if "password" in data:
                hashed_password = generate_password_hash(data["password"], method="sha256")

            # Update employee fields from the JSON data
            employee.first_name = data.get("first_name", employee.first_name)
            employee.last_name = data.get("last_name", employee.last_name)
            employee.email = data.get("email", employee.email)
            employee.phone = data.get("phone", employee.phone)

            # Assign hashed password if provided, else retain the existing password
            employee.password = hashed_password if hashed_password else employee.password

            employee.admin = data.get("admin", employee.admin)

            db.session.commit()

            return {"message": "Customer updated successfully"}, 200

        except Exception as e:
            return {"message": "An error occurred while updating the customer"}, 500


class DeleteEmployeeResource(Resource):
    def delete(self, employee_id):
        try:
            employee = Employees.query.get(employee_id)
            if not employee:
                return {"message": "Employee not found"}, 404

            db.session.delete(employee)
            db.session.commit()

            return {"message": "employee deleted successfully"}, 200

        except Exception as e:
            return {"message": "An error occurred while deleting the employee"}, 500


class CreateEmployeeResource(Resource):
    def post(self):
        try:
            data = request.get_json()

            hashed_password = generate_password_hash(data.get("password"), method="sha256")

            new_employee = Employees(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone=data.get("phone"),
                email=data.get("email"),
                password=hashed_password,
                admin=data.get("admin"),
            )

            db.session.add(new_employee)
            db.session.commit()

            return {"message": "Employee created successfully", "employee_id": new_employee.id}, 201

        except Exception as e:
            return {"message": "An error occurred while creating the employee"}, 500


api.add_resource(CreateEmployeeResource, "/create_employee")
api.add_resource(DeleteEmployeeResource, "/delete_employee/<int:employee_id>")
api.add_resource(EmployeesResource, "/employees", "/employees/<int:employee_id>")
api.add_resource(QueryEmployees, "/query_employees")
api.add_resource(UpdateEmployeeResource, "/update_employee/<int:employee_id>")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

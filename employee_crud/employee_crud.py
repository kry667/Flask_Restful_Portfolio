from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://my-user:my-password@db/my-database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.String(10))

employees_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "phone": fields.String,
    "email": fields.String,
    "password": fields.String,
    "admin": fields.Boolean
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
        search_query = request.args.get('query')
        results = self.query_employees(search_query)
        return results
    
    def query_employees(self, search_query):
        results = Employees.query.filter(
            or_(
            Employees.id == search_query,
            Employees.first_name.like(f'%{search_query}%'),
            Employees.last_name.like(f'%{search_query}%'),
            Employees.phone.like(f'%{search_query}%'),
            Employees.email.like(f'%{search_query}%')
            )
        ).all()
        return results


api.add_resource(EmployeesResource, '/employees', '/employees/<int:employee_id>')
api.add_resource(QueryEmployees, '/query_employees')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
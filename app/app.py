from flask import Flask
from routes.routes import routes_bp  # Import routes blueprint
from routes.customer_routes import customer_routes_bp  # Import routes blueprint
from routes.employee_routes import employee_routes_bp # Import routes blueprint

app = Flask(__name__)

# Register routes blueprint
app.register_blueprint(routes_bp)
app.register_blueprint(employee_routes_bp)
app.register_blueprint(customer_routes_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


























# @app.route('/add_employee', methods=['POST', 'GET'])
# def add():

#     admin_value = request.form.get('admin')

#     is_admin = True if request.form.get('admin').lower() == 'true' else False
 
#     new = Employees(
#         first_name = request.form.get('first_name'),
#         last_name = request.form.get('last_name'),
#         password = request.form.get('password'),
#         admin = is_admin)
#     db.session.add(new)
#     db.session.commit()
#     return redirect("/employees")



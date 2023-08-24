from flask import Flask
from routes.routes import routes_bp  # Import routes blueprint

app = Flask(__name__)

# Register routes blueprint
app.register_blueprint(routes_bp)

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


# @app.route("/update_employee", methods=['POST', 'GET'])
# def update_employee():

#         is_admin = True if request.form.get('admin').lower() == 'true' else False

#         id = request.form.get('id')

#         employee = Employees.query.get(id)
#         employee.first_name = request.form.get('first_name')
#         employee.last_name = request.form.get('last_name')
#         employee.password = request.form.get('password')
#         employee.admin = is_admin
#         db.session.commit()

#         return redirect(f"employee_edit/{id}")

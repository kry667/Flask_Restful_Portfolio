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

#     if admin_value.lower() == 'true':
#         is_admin = True
#     else:
#         is_admin = False
 
#     new = Employees(
#         first_name = request.form.get('first_name'),
#         last_name = request.form.get('last_name'),
#         password = request.form.get('password'),
#         admin = is_admin)
#     db.session.add(new)
#     db.session.commit()
#     return redirect("/employees")



# @app.route("/query_employees", methods=['POST', 'GET'])
# def query_employees():
#     search_query = request.form.get("search")

#     results = Employees.query.filter(
#         or_(
#             Employees.id == search_query,
#             Employees.first_name.like(f'%{search_query}%'),
#             Employees.last_name.like(f'%{search_query}%'),
#             Employees.admin.like(f'%{search_query}%')
#         )
#     ).all()

#     if not results:
#         message = "No results found."
#     else:
#         message = None

#     results_count = len(results)

#     return render_template('employees.html', results=results, message=message, results_count=results_count)





# @app.route("/employees")
# def employees():
#     results = Employees.query.all()

#     if not results:
#         message = "No results found."
#     else:
#         message = None

#     results_count = len(results)

#     return render_template('employees.html', results=results, message=message, results_count=results_count)



# @app.route("/employee_edit/<int:id>", methods=['GET', 'POST'])
# def edit_employee(id):
#     result = Employees.query.get(id)

#     return render_template('employee_edit.html', result=result, id=id)







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

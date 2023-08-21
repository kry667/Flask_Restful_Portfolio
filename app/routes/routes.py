from flask import Blueprint, render_template, request, redirect
import requests

routes_bp = Blueprint('routes', __name__)

####################################### Redirection Routes #########################################

@routes_bp.route('/')
def index():
    return render_template('index.html', results=None)

@routes_bp.route('/admin')
def admin():
    return render_template('admin.html', results=None)

@routes_bp.route('/create_employee')
def create_employee():
    return render_template('create_employee.html')



################################ Customer CRUD Requests Routes #####################################

@routes_bp.route("/customers")
def customers():
    # Make a request to the user_crud API to get all customers data
    user_crud_url = "http://user_crud:5000/customers"
    response = requests.get(user_crud_url)

    if response.status_code == 200:
        customers_data = response.json()
        if not customers_data:
            message = "No results found."
        else:
            message = None
        results_count = len(customers_data)
    else:
        message = response.status_code
        customers_data = []
        results_count = 0

    return render_template('customers.html', results=customers_data, message=message, results_count=results_count)


@routes_bp.route("/query_customers", methods=['POST', 'GET'])
def query_users():
    search_query = request.form.get('search') if request.form.get('search') is not None else request.args.get('query')

    # Make a request to the user_crud API to get search results
    user_crud_url = "http://user_crud:5000/query_customers"
    params = {'query': search_query}
    response = requests.get(user_crud_url, params=params)

    if response.status_code == 200:
        customers_data = response.json()
        if not customers_data:
            message = "No results found."
            results_count = 0
        else:
            message = None
            results_count = len(customers_data)
    else:
        message = response.status_code
        customers_data = []
        results_count = 0

    return render_template('customers.html', results=customers_data, message=message, results_count=results_count, query=search_query)

@routes_bp.route("/customer_edit/<int:customer_id>", methods=['GET', 'POST'])
def edit_customer(customer_id):
    search_query = request.args.get("query")
    user_crud_url = f"http://user_crud:5000/customer_edit/{customer_id}"
    response = requests.get(user_crud_url)

    if response.status_code == 200:
        customer_data = response.json()
        result = customer_data[0]
        message = None
    else:
        message = f"Error: {response.status_code}"
        result = {}

    return render_template('customer.html', result=result, customer_id=customer_id, query=search_query, message=message)

@routes_bp.route("/update_customer", methods=['POST'])
def update_customer():
    customer_id = request.form.get('customer_id')
    # Get the updated data from the form
    updated_data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'city': request.form.get('city'),
        'street': request.form.get('street'),
        'zip_code': request.form.get('zip_code'),
        'state': request.form.get('state')
    }

    # Make a request to the user_crud API to update the customer data
    user_crud_url = f"http://user_crud:5000/update_user/{customer_id}"
    response = requests.patch(user_crud_url, json=updated_data)

    if response.status_code == 200:
        # Customer data updated successfully
        return redirect(f"/customer_edit/{customer_id}?query={request.form.get('search')}")
    else:
        message = f"Error: {response.status_code}"
        return render_template('customer.html', result=updated_data, customer_id=customer_id, message=message)


@routes_bp.route("/delete_user/<int:customer_id>", methods=['POST'])
def delete_customer(customer_id):
    # Make a request to the user_crud API to delete the customer
    user_crud_url = f"http://user_crud:5000/delete_user/{customer_id}"
    response = requests.delete(user_crud_url)

    if response.status_code == 200:
        # Customer deleted successfully
        return redirect(f"/customers?query={request.form.get('search')}")
    else:
        user_crud_url = f"http://user_crud:5000/customer_edit/{customer_id}"
        response = requests.get(user_crud_url)

        if response.status_code == 200:
            customer_data = response.json()
            result = customer_data[0]
        message = f"Error: {response.status_code}"
        return render_template('customer.html', customer_id=customer_id, result=result, message=message)



###################################### Employees CRUD Requests Routes #####################################


@routes_bp.route("/employees")
def all_employees():
    # Make a request to the user_crud API to get all customers data
    employee_crud_url = "http://employee_crud:5000/employees"
    response = requests.get(employee_crud_url)

    if response.status_code == 200:
        employees_data = response.json()
        if not employees_data:
            message = "No results found."
        else:
            message = None
        results_count = len(employees_data)
    else:
        message = response.status_code
        employees_data = []
        results_count = 0

    return render_template('employees.html', results=employees_data, message=message, results_count=results_count)

@routes_bp.route("/query_employees", methods=['POST', 'GET'])
def query_employees():

    search_query = request.form.get('search') if request.form.get('search') is not None else request.args.get('query')
    # Make a request to the user_crud API to get search results
    employee_crud_url = "http://employee_crud:5000/query_employees"
    params = {'query': search_query}
    response = requests.get(employee_crud_url, params=params)

    if response.status_code == 200:
        employees_data = response.json()
        if not employees_data:
            message = "No results found."
            results_count = 0
        else:
            message = None
            results_count = len(employees_data)
    else:
        message = response.status_code
        employees_data = []
        results_count = 0

    return render_template('employees.html', results=employees_data, message=message, results_count=results_count, query=search_query)

# The route which fetch single employee data from Restful Api and renders Employee Edition website with this data
@routes_bp.route("/employee_edit/<int:employee_id>", methods=['GET', 'POST'])
def edit_employee(employee_id):
    search_query = request.args.get("query")
    user_crud_url = f"http://employee_crud:5000/employees/{employee_id}"
    response = requests.get(user_crud_url)

    if response.status_code == 200:
        employee_data = response.json()
        result = employee_data[0]
        message = None
    else:
        message = f"Error: {response.status_code}"
        result = {}

    return render_template('employee_edit.html', result=result, employee_id=employee_id, query=search_query, message=message)
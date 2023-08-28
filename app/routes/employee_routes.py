import requests
from flask import Blueprint, redirect, render_template, request

employee_routes_bp = Blueprint("employee_routes", __name__)


@employee_routes_bp.route("/employees")
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

    return render_template("employees.html", results=employees_data, message=message, results_count=results_count)


@employee_routes_bp.route("/query_employees", methods=["POST", "GET"])
def query_employees():
    search_query = request.form.get("search") or request.args.get("query")
    # Make a request to the user_crud API to get search results
    employee_crud_url = "http://employee_crud:5000/query_employees"
    params = {"query": search_query}
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

    return render_template(
        "employees.html", results=employees_data, message=message, results_count=results_count, query=search_query
    )


# Fetch single employee data from Restful Api and renders Employee Edition page with this data
@employee_routes_bp.route("/employee_edit/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    search_query = request.args.get("query")
    user_crud_url = f"http://employee_crud:5000/employees/{employee_id}"
    response = requests.get(user_crud_url)

    if response.status_code == 200:
        employee_data = response.json()
        result = employee_data[0]
        message = result.get("message", f"Status: {response.status_code}")
    else:
        message = f"Error: {response.status_code}"
        result = {}

    return render_template(
        "employee_edit.html", result=result, employee_id=employee_id, query=search_query, message=message
    )


@employee_routes_bp.route("/update_employee", methods=["POST"])
def update_employee():
    employee_id = request.form.get("employee_id")
    is_admin = True if request.form.get("admin").lower() == "true" else False
    # Get the updated data from the form
    updated_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "password": request.form.get("password"),
        "admin": is_admin,
    }

    # Make a request to the user_crud API to update the employee data
    user_crud_url = f"http://employee_crud:5000/update_employee/{employee_id}"
    response = requests.patch(user_crud_url, json=updated_data)

    if response.status_code == 200:
        # Employee data updated successfully
        return redirect(f"/employee_edit/{employee_id}?query={request.form.get('search')}")
    else:
        message = f"Error: {response.status_code}"
        return render_template("employee_edit.html", result=updated_data, employee_id=employee_id, message=message)


@employee_routes_bp.route("/delete_employee/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    # Request to the employee_crud Restful_API to delete the employee
    employee_crud_url = f"http://employee_crud:5000/delete_employee/{employee_id}"
    response = requests.delete(employee_crud_url)

    if response.status_code == 200:
        # employee deleted successfully
        return redirect(f"/query_employees?query={request.form.get('query')}")
    else:
        employee_crud_url = f"http://employee_crud:5000/employee_edit/{employee_id}"
        response = requests.get(employee_crud_url)

        if response.status_code == 200:
            employee_data = response.json()
            result = employee_data[0]
        message = f"Error: {response.status_code}"
        return render_template("employee_edit.html", employee_id=employee_id, result=result, message=message)


@employee_routes_bp.route("/create_employee", methods=["POST"])
def create_employee():
    # Get the employee data from the form or JSON payload
    employee_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "phone": request.form.get("phone"),
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "admin": True if request.form.get("admin").lower() == "true" else False,
    }

    # Make a request to the employee_crud API to create a new employee
    employee_crud_url = "http://employee_crud:5000/create_employee"
    response = requests.post(employee_crud_url, json=employee_data)

    if response.status_code == 201:
        # Employee created successfully
        return redirect("/employees")  # Redirect to the list of employees
    else:
        message = f"Error: {response.status_code}"
        return render_template("create_employee.html", message=message, employee_data=employee_data)

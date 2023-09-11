import requests
from flask_jwt_extended import jwt_required
from flask import Blueprint, redirect, render_template, request, current_app, session

employee_routes_bp = Blueprint("employee_routes", __name__)


@employee_routes_bp.route("/login", methods=["POST", "GET"])
def login():
    # Get the user input from the login form
    employee_id = request.form.get("login")
    password = request.form.get("password")

    if not employee_id or not password:
        return render_template("index.html")

    credentials = {
        "login": employee_id,
        "password": password
    }

    try:
        # Make a request to the /auth/login endpoint
        response_from_auth = requests.get("http://auth:5000/login", params=credentials)
        
        if response_from_auth.status_code != 200:
            # If the authentication fails, return an error message
            return render_template("index.html", message="Invalid credentials!")

        auth_data = response_from_auth.json()
        token_identifier = auth_data.get("token_identifier")
        session["token_identifier"] = token_identifier

        if not token_identifier:
            # If the token identifier is missing, return an error message
            return render_template("index.html", message="Invalid token identifier!")
        
        token = current_app.config.get("JWT_BLACKLIST_STORE").get(token_identifier)

        if not token:
            # If the token is missing, return an error message
            return render_template("index.html", message="Invalid token!")

        
        admin_url = "http://app:5000/admin"  # Use the appropriate URL
        headers = {"Authorization": f"Bearer {token}"}
        response_to_admin = requests.get(admin_url, headers=headers)

        if response_to_admin.status_code == 200:
            
            return render_template("admin.html")

    except Exception as e:
        pass

    # If there's any other error, return an error message
    return render_template("index.html", message="An error occurred during login.")



# Make a request to the user_crud API to get all employees data and send it to the front-end
@employee_routes_bp.route("/employees")
def all_employees():

    headers = set_request_headers()
    
    employee_crud_url = "http://employee_crud:5000/employees"
    response = requests.get(employee_crud_url, headers=headers)

    if response.status_code != 200:
        return render_template("employees.html", results=[], message=response.status_code, results_count=0)

    employees_data = response.json()
    results_count = len(employees_data)
    message = None if results_count > 0 else "No results found."

    return render_template("employees.html", results=employees_data, message=message, results_count=results_count)



@employee_routes_bp.route("/query_employees", methods=["POST", "GET"])
def query_employees():
    search_query = request.form.get("search") or request.args.get("query")

    headers = set_request_headers()
    
    # Make a request to the user_crud API to get search results
    employee_crud_url = "http://employee_crud:5000/query_employees"
    params = {"query": search_query}
    response = requests.get(employee_crud_url, headers=headers, params=params)

    if response.status_code != 200:
        return render_template("employees.html", results=[], message=response.status_code, results_count=0, query=search_query)

    employees_data = response.json()
    results_count = len(employees_data)
    message = None if results_count > 0 else "No results found."

    return render_template("employees.html", results=employees_data, message=message, results_count=results_count, query=search_query)



# Fetch single employee data from Restful Api and renders Employee Edition page with this data
@employee_routes_bp.route("/employee_edit/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    search_query = request.args.get("query")

    headers = set_request_headers()

    user_crud_url = f"http://employee_crud:5000/employees/{employee_id}"
    response = requests.get(user_crud_url, headers=headers)

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
    # Get the updated data from the HTML form and format it to json 
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

def set_request_headers():
    """
    Retrieve the token_identifier from the user's session,
    fetch the JWT access_token associated with it from Redis,
    and return a request header with the access token for authentication.

    Returns:
        dict: A dictionary containing the request header with the JWT access token.
    """
    token_identifier = session["token_identifier"]
    token = current_app.config.get("JWT_BLACKLIST_STORE").get(token_identifier)
    return {"Authorization": f"Bearer {token}"}
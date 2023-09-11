import requests
from flask import Blueprint, redirect, render_template, request, current_app, session

customer_routes_bp = Blueprint("customer_routes", __name__)


@customer_routes_bp.route("/customers")
def customers():
    # Retrieve the token identifier from the session
    token_identifier = session.get("token_identifier")

    # Retrieve the access token using the token identifier from app config
    access_token = current_app.config["JWT_BLACKLIST_STORE"].get(token_identifier)

    # Make a request to the user_crud API using the access token
    user_crud_url = "http://user_crud:5000/customers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_crud_url, headers=headers)

    # Process the response data
    if response.status_code == 200:
        customers_data = response.json()
        message = "No results found." if not customers_data else None
        results_count = len(customers_data)
    else:
        message = response.text
        customers_data = []
        results_count = 0

    return render_template("customers.html", results=customers_data, message=message, results_count=results_count)



@customer_routes_bp.route("/query_customers", methods=["POST", "GET"])
def query_users():
    search_query = request.form.get("search") or request.args.get("query")
    
    token_identifier = session.get("token_identifier")
    access_token = current_app.config.get("JWT_BLACKLIST_STORE").get(token_identifier)
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Make a request to the user_crud API to get search results
    user_crud_url = "http://user_crud:5000/query_customers"
    params = {"query": search_query}
    response = requests.get(user_crud_url, headers=headers, params=params)

    message = None
    results_count = 0
    customers_data = []

    if response.status_code == 200:
        customers_data = response.json()
        if not customers_data:
            message = "No results found."
        else:
            results_count = len(customers_data)
    else:
        message = response.status_code

    return render_template(
        "customers.html", results=customers_data, message=message, results_count=results_count, query=search_query
    )



@customer_routes_bp.route("/customer_edit/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    search_query = request.args.get("query")

    with current_app.app_context():
        token_identifier = session.get("token_identifier")
        access_token = current_app.config.get("JWT_BLACKLIST_STORE").get(token_identifier)
        user_crud_url = f"http://user_crud:5000/customer_edit/{customer_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_crud_url, headers=headers)

    if response.status_code == 200:
        customer_data = response.json()
        result = customer_data[0]
        message = None
    else:
        message = f"Error: {response.status_code}"
        result = {}

    return render_template("customer.html", result=result, customer_id=customer_id, query=search_query, message=message)


@customer_routes_bp.route("/update_customer", methods=["POST"])
def update_customer():
    customer_id = request.form.get("customer_id")
    # Get the updated data from the form
    updated_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "city": request.form.get("city"),
        "street": request.form.get("street"),
        "zip_code": request.form.get("zip_code"),
        "state": request.form.get("state"),
    }

    # Make a request to the user_crud API to update the customer data
    user_crud_url = f"http://user_crud:5000/update_user/{customer_id}"
    response = requests.patch(user_crud_url, json=updated_data)

    if response.status_code == 200:
        # Customer data updated successfully
        return redirect(f"/customer_edit/{customer_id}?query={request.form.get('search')}")

    message = f"Error: {response.status_code}"
    return render_template("customer.html", result=updated_data, customer_id=customer_id, message=message)


@customer_routes_bp.route("/delete_user/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    # Make a request to the user_crud API to delete the customer
    user_crud_url = f"http://user_crud:5000/delete_user/{customer_id}"
    response = requests.delete(user_crud_url)

    if response.status_code == 200:
        # Customer deleted successfully
        return redirect(f"/query_customers?query={request.form.get('query')}")

    user_crud_url = f"http://user_crud:5000/customer_edit/{customer_id}"
    response = requests.get(user_crud_url)

    if response.status_code == 200:
        customer_data = response.json()
        result = customer_data[0]

    message = f"Error: {response.status_code}"
    return render_template("customer.html", customer_id=customer_id, result=result, message=message)

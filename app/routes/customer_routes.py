import requests
from flask import Blueprint, redirect, render_template, request, current_app

customer_routes_bp = Blueprint("customer_routes", __name__)



@customer_routes_bp.route("/customers")
def customers():
    # Make a request to the user_crud API to get all customers data
    with current_app.app_context():
        access_token = current_app.config.get("MY_GLOBAL_TOKEN")
        user_crud_url = "http://user_crud:5000/customers"
        headers = {"Authorization": f"Bearer b%27eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NDM2MjE5MCwianRpIjoiYjA0YzNkYTAtOTQ4ZC00NmY4LWE4NjYtMmM5MjI4ZWUzM2Q2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6W3siaWQiOjEsImZpcnN0X25hbWUiOiJLcnkiLCJsYXN0X25hbWUiOiJXb2xsbGwiLCJwaG9uZSI6IjY2Ni02NjctNjY3IiwiZW1haWwiOiJrcnlAd29sLmNvbSIsInBhc3N3b3JkIjoic2hhMjU2JHRqRmJHdE9YVHc2c1RkQUQkYjE1ODQ1MTA3MjRkYzMxMTllN2U5YWY4ZGZmMDkyOGIxMDYxNzZiZDAwZGYyMTlkMTIwYWIyNzgwMTNkMjcyOSIsImFkbWluIjp0cnVlfV0sIm5iZiI6MTY5NDM2MjE5MCwiZXhwIjoxNjk0MzYyMzEwLCJhZG1pbiI6dHJ1ZX0.0L4T7Iq_SHjlxE5ncBC-t6GejCC58pPAZPNbrTMTUm4%27"}
        response = requests.get(user_crud_url, headers=headers)

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

    return render_template("customers.html", results=customers_data, message=message, results_count=results_count)


@customer_routes_bp.route("/query_customers", methods=["POST", "GET"])
def query_users():
    search_query = request.form.get("search") if request.form.get("search") is not None else request.args.get("query")

    # Make a request to the user_crud API to get search results
    user_crud_url = "http://user_crud:5000/query_customers"
    params = {"query": search_query}
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

    return render_template(
        "customers.html", results=customers_data, message=message, results_count=results_count, query=search_query
    )


@customer_routes_bp.route("/customer_edit/<int:customer_id>", methods=["GET", "POST"])
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

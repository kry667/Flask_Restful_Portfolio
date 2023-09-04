import pytest
import os
from dotenv import load_dotenv
from flask_restful import Api
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
from user_crud import app, db, QueryResource

# Set the ENV environment variable to 'testing'
load_dotenv()
os.environ['ENV'] = 'testing'

# Create a test Flask app with an in-memory SQLite database
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
api.add_resource(QueryResource, '/query_customers', endpoint='query_customers_resource')

# Access the db instance from the application
db = app.extensions['sqlalchemy'].db

# Fixture to create a test client for the resource
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Define a mock function to replace the actual database query
def mock_query_customers(search_query):
    # This is an example of how you can mock the database query
    # You can return predefined data here for testing purposes
    return []

# Define test cases for the resource with a mock database
@patch('user_crud.QueryResource.query_customers')
def test_query_customers_resource_with_query_param(mock_query_customers, client):
    # Mock the database query to return predefined data
    mock_query_customers.return_value = []  # Assuming no matching results for 'John'

    # Test a GET request to the resource with a query parameter
    response = client.get('/query_customers?query=John')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0  # Assuming no matching results for 'John'

# Test case: Valid query with matching results
@patch('user_crud.QueryResource.query_customers')
def test_query_customers_resource_with_matching_results(mock_query_customers, client):
    # Mock the database query to return predefined data with matching results
    mock_query_customers.return_value = [
        {"id": 1, "first_name": "John", "last_name": "Doe", "email": "john@example.com"},
        {"id": 2, "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"}
    ]

    # Test a GET request to the resource with a query parameter
    response = client.get('/query_customers?query=Doe')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2  # Expecting 2 matching results
    assert data[0]["first_name"] == "John"
    assert data[1]["first_name"] == "Jane"

# Test case: Valid query with no matching results
@patch('user_crud.QueryResource.query_customers')
def test_query_customers_resource_with_no_matching_results(mock_query_customers, client):
    # Mock the database query to return an empty list (no matching results)
    mock_query_customers.return_value = []

    # Test a GET request to the resource with a query parameter
    response = client.get('/query_customers?query=Smith')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0  # Expecting no matching results

# Test case: Invalid query parameter (missing query parameter)
def test_query_customers_resource_missing_query_param(client):
    # Test a GET request to the resource without a query parameter
    response = client.get('/query_customers')
    assert response.status_code == 400  # Bad request status code

def test_query_customers_resource_with_no_results(client):
    # Mock the database query to return no results
    mock_query_customers.return_value = []

    # Test a GET request to the resource with a query parameter
    response = client.get('/query_customers?query=NonExistentName')
    assert response.status_code == 500
    # data = response
    assert len(response) == 0  # Expecting no matching results


@patch('user_crud.QueryResource.query_customers')
def test_query_customers_resource_database_error_handling(mock_query_customers, client):
    # Mock the database query to raise a database error
    mock_query_customers.side_effect = SQLAlchemyError("Database error")

    # Test a GET request to the resource with a query parameter
    response = client.get('/query_customers?query=John')
    assert response.status_code == 500  # Expecting a 500 Internal Server Error
    data = response.get_json()
    assert "message" in data  # Ensure there's an error message



# Run the tests with pytest
if __name__ == '__main__':
    pytest.main()

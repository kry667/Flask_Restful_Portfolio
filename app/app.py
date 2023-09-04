from flask import Flask
from routes.customer_routes import customer_routes_bp 
from routes.employee_routes import employee_routes_bp
from routes.routes import routes_bp


app = Flask(__name__)

# Register routes blueprint
app.register_blueprint(routes_bp)
app.register_blueprint(employee_routes_bp)
app.register_blueprint(customer_routes_bp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    
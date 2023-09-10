from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Simulate user authentication
users = {
    'user1': 'pass1',
    'user2': 'password2'
}

@app.route('/login', methods=['POST'])
def login():
    
    username = request.form.get('user')
    password = request.form.get('pass')
    
    if username in users and users[username] == password:
        expires = datetime.timedelta(minutes=30)  # Token expiration time
        access_token = create_access_token(identity=username, expires_delta=expires)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    # This route is protected; only authenticated users with valid tokens can access it
    return jsonify({'message': 'Welcome to the admin route'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)

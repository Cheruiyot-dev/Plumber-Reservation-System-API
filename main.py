from models import (app, db, User, Customer, Plumber)
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta
from functools import wraps

from uuid import uuid4


# Decorator for verifying the jwt
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # token is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        # Return 401 if token not passed
        if not token:
            return jsonify({'message': 'Authentication token is missing'}), 401
        try:
            # Decoding the payload to fetch stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['id']
            current_user = User.query.filter(User.id == user_id).first()
            print(current_user)

        except jwt.DecodeError:
            return jsonify({'message': 'Invalid Token'}), 401
        # Returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/")
@token_required
def home(current_user):
    if current_user is None:
        return jsonify({"message": "No user found"}), 404
    else:
        user = current_user
        return jsonify({"message": "hello world", "username": user.username, "email": user.email, "type": user.type})

# Registration routes


@app.route("/register/plumber", methods=["Post"])
def register_plumber():
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.json
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                # # Check if username or email already exists
                existing_plumber = Plumber.query.filter((Plumber.email == email) | (Plumber.username == username)).first()
                print(type(existing_plumber))
                if existing_plumber is not None:
                    return jsonify({"Error": "username or email already exists"}), 400
                plumber = Plumber(username=username, email=email)
                plumber.set_password(password)
                # Generate and assign a unique public_id
                plumber.public_id = str(uuid4())
                db.session.add(plumber)
                db.session.commit()
                r = "Successfully registered new plumber:" + str(plumber.id)
                res = {"Result": r}

                return jsonify(res), 201

            except Exception as e:
                print(e)
                return jsonify({"Error": str(e)}), 500
        else:
            return jsonify({"Error": "data is not json"}), 400
    else:
        return jsonify({"Error": "Method is not allowed."}), 403


# Register customer
@app.route("/register/customer", methods=["Post"])
def register_customer():
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.json
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                # Check if username or email already exists.
                existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
                print(type(existing_user))
                if existing_user is not None:
                    return jsonify({"Error": "username or email already exists"}), 400

                customer = Customer(username=username, email=email)
                customer.set_password(password)
                customer.public_id = str(uuid4())
                db.session.add(customer)
                db.session.commit()

                r = "Successfully registered new plumber:" + str(customer.id)
                res = {"Result": r}

                return jsonify(res), 201

            except Exception as e:
                # print(e)
                return jsonify({"Error": str(e)}), 500
        else:
            return jsonify({"Error": "data is not json"}), 400
    else:
        return jsonify({"Error": "Method is not allowed."}), 403

# Login routes


def generate_token(user_id):
    return jwt.encode({
        'id': user_id, 'exp': datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])


@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            login_identifier = data.get('login_identifier')
            password = data.get('password')

            # Check if login_identifier is either an email or username
            if '@' in login_identifier:
                user = User.query.filter_by(email=login_identifier).first()
            else:
                user = User.query.filter_by(username=login_identifier).first()

            if user is not None and user.check_password(password):
                if user.type == 'plumber':
                    plumber = Plumber.query.get(user.id)
                    # print("plumber:", plumber)

                    token = generate_token(plumber.id)
                    return jsonify({"token": token, "Success": "Plumber logged in successfully"}), 201
                else:
                    user.type == 'customer'
                    customer = Customer.query.get(user.id)
                    token = token = generate_token(customer.id)
                    return jsonify({"token": token, "message": "Customer login was successful"}), 200
            else:
                return jsonify({"Error": "Invalid login credentials"}), 401
        else:
            return jsonify({"Error": "Data is not JSON"}), 400
    else:
        return jsonify({"Error": "Method is not allowed"}), 403


if __name__ == "__main__":
    app.run(debug=True)
    app.run()

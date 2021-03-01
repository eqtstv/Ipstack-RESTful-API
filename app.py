import os
import sys

import psycopg2
import requests
import waitress
from flask import Flask, jsonify, make_response, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash


IPSTACK_API_KEY = os.environ["IPSTACK_API_KEY"]
IPSTACK_API_URL = "http://api.ipstack.com"
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_DATABASE = os.environ["DATABASE_DATABASE"]


conn = psycopg2.connect(
    host=DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    database=DATABASE_DATABASE,
)


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
jwt = JWTManager(app)


@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]

    if not username:
        return make_response(jsonify({"msg": "Missing username parameter."}), 400)
    if not password:
        return make_response(jsonify({"msg": "Missing password parameter."}), 400)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT Username, Password FROM Users WHERE Username=%s", (username,)
    )

    user = cursor.fetchall()

    if user:
        return make_response(jsonify("User aleady exists"))

    cursor.execute(
        "INSERT INTO Users (username, password) VALUES (%s, %s)",
        (username, generate_password_hash(password, method="sha256")),
    )
    conn.commit()

    return make_response(jsonify("User created"))


@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return make_response(jsonify({"msg": "Missing JSON in request."}), 400)

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return make_response(jsonify({"msg": "Missing username parameter."}), 400)
    if not password:
        return make_response(jsonify({"msg": "Missing password parameter."}), 400)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT Username, Password FROM Users WHERE Username=%s", (username,)
    )
    user = cursor.fetchall()

    if not user or not check_password_hash(user[0][1], password):
        return make_response(jsonify({"msg": "Bad email or password."}), 401)

    access_token = create_access_token(identity=username)
    return make_response(jsonify(access_token=access_token), 200)


@app.route("/protected", methods=["GET"])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/")
def hello_world():
    URL = f"{IPSTACK_API_URL}/134.201.250.155?access_key={IPSTACK_API_KEY}"
    example_response = requests.get(URL).json()
    return example_response


@app.route("/ip/<ip_address>")
def show_ip_address(ip_address):
    url = f"{IPSTACK_API_URL}/{ip_address}?access_key={IPSTACK_API_KEY}"
    response = requests.get(url).json()
    return response


if __name__ == "__main__":
    if sys.argv[1] == "debug":
        app.run(debug=True)

    if sys.argv[1] == "production":
        waitress.serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

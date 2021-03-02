from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from flask_app.db import conn

auth = Blueprint("auth", __name__)


def is_valid_json(username, password):
    if not username or username == "":
        return False
    if not password or len(password) < 8:
        return False
    return True


@auth.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not is_valid_json(username, password):
        return make_response(
            jsonify({"msg": "Wrong username or password parameter."}), 400
        )

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


@auth.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return make_response(jsonify({"msg": "Missing JSON in request."}), 400)

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not is_valid_json(username, password):
        return make_response(
            jsonify({"msg": "Wrong username or password parameter."}), 400
        )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT Username, Password FROM Users WHERE Username=%s", (username,)
    )
    user = cursor.fetchall()

    if not user or not check_password_hash(user[0][1], password):
        return make_response(jsonify({"msg": "Bad email or password."}), 401)

    access_token = create_access_token(identity=username)
    return make_response(jsonify(access_token=access_token), 200)

import json
import os
import sys

import psycopg2
import requests
import waitress
from flask import Flask, jsonify, make_response, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
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


@app.route("/")
def hello_world():
    return "<center><h1>Sofomo assignment</h1></center>"


@app.route("/location", methods=["POST", "DELETE", "GET"])
@jwt_required
def location():
    if not request.is_json:
        return make_response(jsonify({"msg": "Missing JSON in request."}), 400)

    address = request.json.get("address", None)

    if not address:
        return make_response(jsonify({"msg": "Wrong json"}), 400)

    if request.method == "POST":
        url = f"{IPSTACK_API_URL}/{address}?access_key={IPSTACK_API_KEY}"
        response = requests.get(url).json()

        if response["type"] is None:
            return jsonify("Wrong ip address")

        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM geodata WHERE ip=%s", (address,))
        row = cursor.fetchall()

        if row:
            return make_response(jsonify("Ip address already in the database"))

        cursor.execute(
            "INSERT INTO geodata \
            (address, ip, type, continent_code, continent_name, country_code,\
            country_name, region_code, region_name, city, zip, latitude, longitude) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                address,
                response["ip"],
                response["type"],
                response["continent_code"],
                response["continent_name"],
                response["country_code"],
                response["country_name"],
                response["region_code"],
                response["region_name"],
                response["city"],
                response["zip"],
                response["latitude"],
                response["longitude"],
            ),
        )
        conn.commit()
        return make_response(jsonify(f"Address {address} added to the database"))

    elif request.method == "DELETE":
        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM geodata WHERE ip=%s", (address,))
        row = cursor.fetchall()

        if not row:
            return make_response(jsonify("Address not in the database"))

        cursor.execute("DELETE FROM geodata WHERE ip=%s", (address,))
        conn.commit()
        return make_response(jsonify(f"Address {address} deleted from the database"))

    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM geodata WHERE address=%s", (address,))
        r = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        if not r:
            return make_response(jsonify("Address not in the database"))
        return json.dumps(r)


if __name__ == "__main__":
    if sys.argv[1] == "debug":
        app.run(debug=True)

    if sys.argv[1] == "production":
        waitress.serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

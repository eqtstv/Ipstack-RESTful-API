import json
import os

import requests
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required

from flask_app.db import conn

api = Blueprint("api", __name__)

IPSTACK_API_URL = "http://api.ipstack.com"
IPSTACK_API_KEY = os.environ["IPSTACK_API_KEY"]


@api.route("/location", methods=["POST", "DELETE", "GET"])
@jwt_required
def location():
    if not request.is_json:
        return make_response(jsonify("Missing JSON in request."), 400)

    address = request.json.get("address", None)

    if not address:
        return make_response(jsonify("Wrong json"), 400)

    if request.method == "POST":
        url = f"{IPSTACK_API_URL}/{address}?access_key={IPSTACK_API_KEY}"
        response = requests.get(url).json()

        if response["type"] is None:
            return make_response(jsonify("Wrong ip address"), 400)

        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM geodata WHERE address=%s", (address,))
        row = cursor.fetchall()

        if row:
            return make_response(jsonify("Ip address already in the database"), 400)

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
        return make_response(jsonify(f"Address {address} added to the database"), 200)

    elif request.method == "DELETE":
        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM geodata WHERE ip=%s", (address,))
        row = cursor.fetchall()

        if not row:
            return make_response(jsonify("Address not in the database"), 400)

        cursor.execute("DELETE FROM geodata WHERE ip=%s", (address,))
        conn.commit()
        return make_response(
            jsonify(f"Address {address} deleted from the database"), 200
        )

    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM geodata WHERE address=%s", (address,))
        r = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        if not r:
            return make_response(jsonify("Address not in the database"), 400)
        return json.dumps(r[0])

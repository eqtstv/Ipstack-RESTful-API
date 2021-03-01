import os
import sys

import requests
import waitress
from flask import Flask

app = Flask(__name__)

IPSTACK_API_KEY = os.environ["IPSTACK_API_KEY"]


@app.route("/")
def hello_world():
    URL = f"http://api.ipstack.com/134.201.250.155?access_key={IPSTACK_API_KEY}"
    example_response = requests.get(URL).json()
    return example_response


if __name__ == "__main__":
    if sys.argv[1] == "debug":
        app.run(debug=True)

    if sys.argv[1] == "production":
        waitress.serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

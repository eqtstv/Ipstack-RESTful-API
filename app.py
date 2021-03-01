import sys

import waitress
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    if sys.argv[1] == "debug":
        app.run(debug=True)

    if sys.argv[1] == "production":
        waitress.serve(app, host="0.0.0.0", port=8080)

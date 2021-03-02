import os

from flask import Flask
from flask_jwt_extended import JWTManager

from flask_app.api import api
from flask_app.auth import auth

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
jwt = JWTManager(app)


@app.route("/")
def hello_world():
    return "<center><h1>Sofomo assignment</h1></center>"


app.register_blueprint(api)
app.register_blueprint(auth)

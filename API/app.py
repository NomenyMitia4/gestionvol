from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:3000", "http://127.0.0.1:5500"], methods=['GET', 'POST'], supports_credentials=True)


@app.route("/")
def welcome():
    return "This is where the APIs are being hosted"

import controller.user_controller as user_controller

import controller.flight_controller as flight_controller

import controller.gemini_controller as gemini_controller
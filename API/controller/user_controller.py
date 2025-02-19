from app import app
from model.user_model import user_model
from flask import request
import json

@app.route("/user/signup")
def signup():
    user = user_model()
    return user.user_create()

@app.route("/user/login")
def login():
    return "This is login operation"

@app.route("/user/logout")
def logout():
    return "This is logout operation"

@app.route("/user/getAll")
def user_getAll():
    user = user_model()
    return user.user_read()

@app.route("/user/add", methods=["POST"])
def user_add():
    user = user_model()
    try:
        data = request.get_json()
        if not data:
            return json({"error": "No JSON data received"}), 400
        
        result = user.user_create(data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)}), 500


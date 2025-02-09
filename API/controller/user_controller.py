from app import app
from model.user_model import user_model
from flask import request

user = user_model()

@app.route("/user/signup")
def signup():
    obj = user_model()
    return obj.user_create()

@app.route("/user/login")
def login():
    return "This is login operation"

@app.route("/user/logout")
def logout():
    return "This is logout operation"

@app.route("/user/getAll")
def user_getAll():
    user = user.user_read()
    
    return user

@app.route("/user/add", methods=["POST"])
def user_add():
    return user.user_create(request.form)


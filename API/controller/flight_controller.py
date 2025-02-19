from app import app
from model.flight_model import flight_model
from flask import request, jsonify
from flask_cors import cross_origin
import json

@app.route("/flight/getAll")

def flight_getAll():
    flight = flight_model()
    return flight.flight_read()

@app.route("/flight/add", methods=["POST"])
def flight_add():
    flight = flight_model()
    try:
        data = request.get_json()
        if not data:
            return json({"error": "No JSON data received"}), 400
        
        result = flight.flight_create(data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)}), 500
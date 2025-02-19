from app import app
from flask import request
from model.gemini_model import gemini_model
import json

gemini = gemini_model()
@app.route("/gemini")
def init():
    return gemini.test()

@app.route("/gemini/sendMessage", methods=["POST"])
def sendMessage():
    try:
        data = request.get_json()
        if not data:
            return json({"error": "No JSON data received"}), 400
        
        result = gemini.send_msg(data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)}), 500
    
@app.route("/gemini/getMessage")
def getMessage():
    return gemini.getChatHistory()
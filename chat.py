import os
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyD0lpHu4fLOwDG7K-JyeCS5ORdJJXQAEiA")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

    # history=[
        # {
        #   "role": "user",
        #   "parts": [
        #     "hi\n",
        #   ],
        # },
        # {
        #   "role": "model",
        #   "parts": [
        #     "Hi there! How can I help you today?\n",
        #   ],
        # },
    # ]
data = [{"flight_id": 1, "name": "Airlane Madagascar", "price": 12000.0, "type": "entrant", "distance": 16000.0, "date_time":
"2025-03-15T00:00:00", "origin": "Antananarivo", "destination": "Manila"}, {"flight_id": 2, "name": "AirlaneMadagascar", "price": 9100.0, "type": "entrant", "distance": 8000.0, "date_time": "2025-06-15T00:00:00", "origin":
"Antananrivo", "destination": "France"}]

data = json.dumps(data)

history = [{
    "role": "user",
    "parts": ["You are my sql code provider \n"],
    "role": "user",
    "parts": ["I'm working on a project about management of flights. You only provide me the sql code without a long text, just the sql code so i can execute it immediately"],
    "role": "user",
    "parts": ["You dont need to remind me that it is a SQL code. Just give me the code so i can immediately pass it to my database"],
    "role": "user",
    "parts": ["This is my data about the table flight: "+str(data)]
}]

print("Bot: Hi, how can i help you?")

while True:
    user_input = input("Me: ")
    chat_session = model.start_chat(
        history=history
    )
    response = chat_session.send_message(user_input)
    model_response = response.text
    print("Bot:"+model_response)
    
    history.append({"role":"user", "parts": [user_input]})
    history.append({"role":"model", "parts": [model_response]})
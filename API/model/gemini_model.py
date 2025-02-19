from google import genai
import google.generativeai as genai
import json
from model.flight_model import flight_model
import mysql.connector
from flask import jsonify
# AIzaSyD0lpHu4fLOwDG7K-JyeCS5ORdJJXQAEiA

class gemini_model():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="gestionvol")
            self.connection.autocommit = True
            self.cur = self.connection.cursor(dictionary=True)
            print("Connection to database etablished successfully")
        except:
            print("Error connecting to database!!!")
        with open("./APIKey.txt", "r") as API:
            self.apikey = API.read()
            API.close()
        genai.configure(api_key=self.apikey)
        
        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
        )
        
        self.chatHistory = [{
            "role": "model",
            "parts": "Hello! How can I assist you?"
        }]
        
        self.session_start()
        self.history_init()
        
    def history_init(self):
        # flights = flight_model()
        
        # flights = flights.flight_read()
        
        data = [{"flight_id": 1, "name": "Airlane Madagascar", "price": 12000.0, "type": "entrant", "distance": 16000.0, "date_time":
        "2025-03-15T00:00:00", "origin": "Antananarivo", "destination": "Manila"}, {"flight_id": 2, "name": "AirlaneMadagascar", "price": 9100.0, "type": "entrant", "distance": 8000.0, "date_time": "2025-06-15T00:00:00", "origin":
        "Antananrivo", "destination": "France"}]

        data1 = [{
            "code": "AAI",
            "country": "Denmark",
            "city": "Aalborg"
        }]
        
        data2 = [{
            "avion_id": "airbus A320",
            "max_seat": 70
        }]
        
        # data = flights.get_data(as_text=True)
        self.history = [{
            "role": "user",
            "parts": ["You are my sql code provider. You will provide me a SELECT query"]},
            {
                "role": "user",
                "parts": ["I'm working on a project about management of flights. You only provide me the sql code without a long text, just the sql code so i can execute it immediately"],
            },
            {
                "role": "user",
                "parts": ["You dont need to remind me that it is a SQL code. Just give me the raw code so i can directly pass it to my database"],   
            },
            {
                "role": "user",
                "parts": ["This is model of my data about the table flight: "+str(data)],   
            },
            {
                "role": "user",
                "parts": ["This is model of my data about the table airport: "+str(data1)],   
            },
            {
                "role": "user",
                "parts": ["This is model of my data about the table avion: "+str(data2)],   
            },
            {
                "role": "user",
                "parts": ["As u can see, I have three tables(flight, airport, avion). Flight has an INNER JOIN with table avion on avion column"],   
            },
            {
                "role": "user",
                "parts": ["Also, Flight has an INNER JOIN with table airport on origin and destination column. You should remember these links."],   
            },
            {
                "role": "user",
                "parts": ["SO whenever you do a SELECT query on flight table you use that INNER JOIN on table avion and airport. Always"],   
            },
            {
                "role": "user",
                "parts": ["Also, use the appropriate value on the table when you do the query"],   
            },
            {
                "role": "user",
                "parts": ["You dont need to add sql to the syntax when you give me the answser. You dont need to say based on te information i provide you. All you do is just give me the syntax of the SQL query necessary"]   
            },
            {
                "role": "user",
                "parts": ["Chiffre Affaire = price of the flight * reserved_seat"]
            },
            {
                "role": "user",
                "parts":["Fixed Price or Coût fixe = 10 000 * max_seat"],
            },
            {
                "role": "user",
                "parts": ["Benefice = CA - Coût Fixe"]
            },
            {
                "role": "user",
                "parts": [">Our price's unity is Ariary. When i only ask you about CA, Benefice or Fixed you dont return a SQL to me but you calculate with these formula i gave you. Instead, you directly return to me the result with some explanation about it"],
            },
            {
                "role":"user",
                "parts": ["This is an example of how you should answer: sql'SELECT * FROM flight' , sql'SELECT COUNT(*) FROM flight', sql'SELECT * FROM flight WHERE id=id',  sql'SELECT * FROM flight as f INNER JOIN avion as a ON f.avion = a.avion_id'. And more complex SELECT query... "]
            },
        ]
        
        query_sql = "SELECT f.*, airdepart.city AS departure_airport_city, airdepart.country AS departure_airport_country, airdest.city AS destination_airport_city ,airdest.country AS destination_airport_country, av.* FROM flight as f INNER JOIN airport AS airdepart ON f.origin = airdepart.code INNER JOIN airport AS airdest ON f.destination = airdest.code INNER JOIN avion AS av ON f.avion = av.avion_id"
        self.cur.execute(query_sql)
        result = self.cur.fetchall()
        for res in result:
            self.history.append({"role": "model", "parts": [str(res)]})
    
    def session_start(self):
        self.history_init()
        self.chat_session = self.model.start_chat(
            history = self.history
        )
    
    def getChatHistory(self):
        return self.chatHistory
        
    def send_msg(self, msg):
        print(msg["message"])
        response = self.chat_session.send_message(msg["message"])
        model_response = response.text
        #update chat history
        self.history.append({"role": "user", "parts": [msg["message"]]})
        self.chatHistory.append({"role": "user", "parts": [msg["message"]]})
        print(self.chatHistory)
        query_sql = model_response
        print(query_sql)

        try:
            cleaned_query = query_sql.replace("sql", "").strip() 
            cleaned_query = cleaned_query.replace("```", "").strip()
            # print(cleaned_query)
            self.cur.execute(cleaned_query)
            model_response = cleaned_query
            result = self.cur.fetchall() 
            print(result)
            # if cleaned_query == "SELECT * FROM flight;" or cleaned_query == "SELECT * FROM flight":
            #     flights = flight_model()
            #     result = flights.flight_read()
            #     print(result)
            self.history.append({"role": "model", "parts": [model_response]})

            print("ato")
            print(result)
            values = (list(result[0].values())[0])  # Convert values to a list and access the first element   
            print(values)
            self.history.append({"role": "model", "parts": [f"{str(values)}"]})
            self.history.append({"role": "user", "parts": [f"Now, i allow you to explain the result {str(values)} with human language. Dont use ID, use a name instead. For example, we have actually 10 flights"]})
            response = self.chat_session.send_message(f"Now, i allow you to explain the result {str(values)} with human language. Dont use ID, use a name instead. For example, we have actually 10 flights")
            self.chatHistory.append({"role": "model", "parts": [f"{str(response.text)}"]})
            return {
                "status":200,
                "message": "Message envoyé"
            }
        except:
            self.history.append({"role": "model", "parts": [model_response]})
            self.chatHistory.append({"role": "model", "parts": [model_response]})
            return {
                "status":200,
                "message": "Message envoyé"
            }
        
        finally:
            return  {
                "error": "Error"
            } 

    def test(self):
        client = genai.Client(api_key=self.apikey)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents="Explain how AI works"
        )
        print(response.text)

        return response.text
    

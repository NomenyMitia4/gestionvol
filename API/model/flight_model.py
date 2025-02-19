import mysql.connector
import json
from flask import jsonify
import json

class flight_model():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="gestionvol")
            self.connection.autocommit = True
            self.cur = self.connection.cursor(dictionary=True)
            print("Connection to database etablished successfully")
        except:
            print("Error connecting to database!!!")
            
    def flight_read(self):
        query_sql = "SELECT f.*, airdepart.city AS departure_airport_city, airdepart.country AS departure_airport_country, airdest.city AS destination_airport_city ,airdest.country AS destination_airport_country, av.* FROM flight as f INNER JOIN airport AS airdepart ON f.origin = airdepart.code INNER JOIN airport AS airdest ON f.destination = airdest.code INNER JOIN avion AS av ON f.avion = av.avion_id"
        self.cur.execute(query_sql)
        result = self.cur.fetchall()
        for res in result:
            res["departure_time"] = res["departure_time"].isoformat()
            
        if len(result) > 0:
            formatted_results = []
            for row in result:
                formatted_results.append({
                    "flight_id": row["flight_id"],
                    "avion": {
                        "avion_id": row["avion"],
                        "max_seat": row["max_seat"]
                        },
                    "price": row["price"],
                    "type": row["type"],
                    "distance": row["distance"],
                    "origin": {
                        "country": row["departure_airport_country"],
                        "city": row["departure_airport_city"]
                    },
                    "destination": {
                        "country": row["destination_airport_country"],
                        "city": row["destination_airport_city"]
                    },
                    "departure_time": row["departure_time"],
                    "reserved_seat": row["reserved_seat"],
                    "free_seat": row["free_seat"]
                })
            return jsonify(formatted_results)
        else:
            return "No data found"
        
    def flight_create(self, data):
        try:
            query_sql = "INSERT INTO flight(name, price, type, distance, date_time, origin, destination) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(query_sql, (data["name"], data["price"], data["type"], data["distance"], data["departure_time"], data["origin"], data["destination"]))
            return "Flight added successfully"
        except:
            return "An error has occured"
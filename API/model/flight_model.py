import mysql.connector
import json

class flight_model():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="gestionvol")
            self.cur = self.connection.cursor(dictionary=True)
            print("Connection to database etablished successfully")
        except:
            print("Error connecting to database!!!")
            
    def flight_read(self):
        query_sql = "SELECT * FROM flight"
        self.cur.execute(query_sql)
        result = self.cur.fetchall()
        # print(result)
        
        if len(result) > 0:
            return json.dumps(result)
        else:
            return "No data found"
        
    def flight_create(self):
        pass
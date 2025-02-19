from flask import jsonify
import mysql.connector # type: ignore
import json

class user_model():
    
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host="127.0.0.1", user="root", password="", database="gestionvol")
            self.connection.autocommit = True
            self.cur = self.connection.cursor(dictionary=True)
            print("Connection to database etablished successfully")
        except:
            print("Error connecting to database!!!")
        
    def user_create(self, data):
        try:
            query_sql = "INSERT INTO user(name, password) VALUES(%s, %s)"
            self.cur.execute(query_sql, (data['name'], data['password']))
            return "User added successfully"
        except:
            return "An error has occured"
    
    def user_read(self):
        query_sql = """
        SELECT 
        u.user_id, u.name, u.password, u.car,
        c.car_id, c.name
        FROM user AS u
        INNER JOIN car AS c ON u.car = c.car_id
        """
        # query_sql = "SELECT u.name, c.name FROM user AS u INNER JOIN car AS c on u.car = c.car_id"
        self.cur.execute(query_sql)
        result = self.cur.fetchall()
        # print(result)
        
        if len(result) > 0:
            formatted_results = []
            for row in result:
                formatted_results.append({
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "password": row["password"],
                    "car": {
                        "car_id": row["car_id"],
                        "car_name": row["name"],
                    }
                })
            return jsonify(formatted_results)
        else: 
            return "No data found"
    
    def user_delete(self):
        pass
    
    def user_update(self):
        pass
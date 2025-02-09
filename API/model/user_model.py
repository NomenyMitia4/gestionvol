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
        query_sql = "SELECT * FROM user"
        self.cur.execute(query_sql)
        result = self.cur.fetchall()
        # print(result)
        
        if len(result) > 0:
            return json.dumps(result)
        else: 
            return "No data found"
    
    def user_delete(self):
        pass
    
    def user_update(self):
        pass
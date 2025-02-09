from app import app
from model.flight_model import flight_model

@app.route("/flight/list")
def read():
    flight = flight_model()
    flight = flight.flight_read()
    
    return flight
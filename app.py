from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

TOTAL_SLOTS = 5
parked_cars = {}

def calculate_fee(hours):
    if hours < 0:
        raise ValueError("Parking duration cannot be negative")
    if hours <= 0.5:
        return 0
    elif hours <= 2:
        return 50
    elif hours <= 4:
        return 100
    elif hours <= 6:
        return 300
    else:
        return 500

@app.route("/")
def home():
    return f"<h1>Parking System</h1><p>Available slots: {TOTAL_SLOTS - len(parked_cars)}</p><p>Parked cars: {parked_cars}</p>"

@app.route("/park", methods=["GET", "POST"])
def park():
    if request.method == "POST":
        plate = request.form["plate"]
        if len(parked_cars) < TOTAL_SLOTS:
            parked_cars[plate] = datetime.now()
            return f"<p>Vehicle {plate} parked successfully.</p>"
        else:
            return "<p>Parking Slots full. Try again later.</p>"
    return '''
        <h1>Park a car</h1>
        <form method="POST">
            <input type="text" name="plate" placeholder="Enter plate number">
            <button type="submit">Park</button>
        </form>
    '''

@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        plate = request.form["plate"]
        if plate in parked_cars:
            entry_time = parked_cars[plate]
            exit_time = datetime.now()
            duration = exit_time - entry_time
            hours_parked = duration.total_seconds() / 3600
            fee = calculate_fee(hours_parked)
            del parked_cars[plate]
            return f"<p>Vehicle {plate} parked for {hours_parked:.2f} hours. Fee: {fee}</p>"
        else:
            return "<p>Vehicle not found</p>"
    return '''
        <h1>Remove a car</h1>
        <form method="POST">
            <input type="text" name="plate" placeholder="Enter plate number">
            <button type="submit">Remove</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
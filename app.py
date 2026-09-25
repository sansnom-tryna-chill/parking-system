from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

TOTAL_SLOTS = 10
parked_cars = {1: None, 2: None, 3: None, 4: None, 5: None, 6:None, 7:None, 8:None, 9:None, 10:None}

STYLE = '''
<style>
    body { font-family: Arial, sans-serif; max-width: 500px; margin: 60px auto; padding: 0 20px; color: #222; }
    h1 { color: #1a5c1a; }
    nav a { margin-right: 15px; text-decoration: none; color: #1a5c1a; font-weight: bold; }
    input, button { padding: 8px; font-size: 1em; margin-top: 8px; }
    button { background: #1a5c1a; color: white; border: none; cursor: pointer; border-radius: 4px; }
    p { background: #f4f4f4; padding: 10px; border-radius: 4px; }
</style>
<nav>
    <a href="/">Home</a>
    <a href="/park">Park</a>
    <a href="/remove">Remove</a>
</nav>
'''

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
    slots_html = ""

    for slot, car in parked_cars.items():
        if car is None:
            slots_html += f"""
            <a href="/park?slot={slot}" style="
                display:inline-block;
                width:150px;
                padding:25px;
                margin:10px;
                background:green;
                color:white;
                text-decoration:none;
                text-align:center;
                border-radius:10px;
                font-size:20px;
                font-weight:bold;
            ">
                Slot {slot}<br>
                AVAILABLE
            </a>
            """
        else:
            slots_html += f"""
            <div style="
                display:inline-block;
                width:150px;
                padding:25px;
                margin:10px;
                background:red;
                color:white;
                text-align:center;
                border-radius:10px;
                font-size:20px;
                font-weight:bold;
            ">
                Slot {slot}<br>
                OCCUPIED
            </div>
            """

    return f"""
    <html>
    <head>
        <title>Parking Dashboard</title>
    </head>

    <body style="font-family:Arial; text-align:center;">

        <h1>Parking Dashboard</h1>

        <p>Select an available parking slot:</p>

        <div>
            {slots_html}
        </div>

        <br>

        <a href="/remove">Remove Vehicle</a>

    </body>
    </html>
    """

@app.route("/park", methods=["GET", "POST"])
def park():
    if request.method == "POST":
        plate = request.form["plate"]
        slot = int(request.form["slot"])

        if parked_cars[slot] is not None:
            return "<h2>Sorry, that slot is already occupied.</h2><a href='/'>Go to Home</a>"

        parked_cars[slot] = {
            "plate": plate,
            "entry_time": datetime.now()
        }

        return f"""
           {STYLE}
        <h2>Vehicle Parked Successfully!</h2>
        <p>Vehicle: {plate}</p>
        <p>Parking Slot: {slot}</p>
        <a href="/">Go to Home</a>
        """

    slot = request.args.get("slot")

    if slot is None:
        return "<h2>Please select a parking slot first.</h2><a href='/'>Go to Home</a>"

    slot = int(slot)

    if parked_cars[slot] is not None:
        return "<h2>Sorry, that slot is already occupied.</h2><a href='/'>Go to Home</a>"

    return f"""
       {STYLE}
    <h2>Park Your Vehicle</h2>

    <p>Selected Slot: <strong>{slot}</strong></p>

    <form method="POST">

        <input type="hidden" name="slot" value="{slot}">

        <input type="text"
               name="plate"
               placeholder="Enter plate number"
               required>

        <br><br>

        <button type="submit">Park Vehicle</button>

    </form>

    <br>

    <a href="/">Back to Dashboard</a>
    """

@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        plate = request.form["plate"]

        for slot, car in parked_cars.items():
            if car is not None and car["plate"] == plate:
                entry_time = car["entry_time"]
                exit_time = datetime.now()

                duration = exit_time - entry_time
                hours_parked = duration.total_seconds() / 3600

                fee = calculate_fee(hours_parked)

                parked_cars[slot] = None

                return f"""
                {STYLE}
                <h2>Vehicle Removed Successfully</h2>
                <p>Vehicle {plate} was parked for {hours_parked:.2f} hours.</p>
                <p>Fee: {fee}</p>
                <a href="/">Go to Home</a>
                """

        return "<p>Vehicle not found</p>"

    return f"""
           {STYLE}
    <h2>Remove a car</h2>
    <form method="POST">
        <input type="text" name="plate" placeholder="Enter plate number">
        <button type="submit">Remove</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'data.json'

# Load data from JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"events": [], "registrations": {}}

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    data = load_data()
    return render_template("index.html", events=data["events"], registrations=data["registrations"])

@app.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        data = load_data()
        new_id = len(data["events"]) + 1
        new_event = {
            "id": new_id,
            "title": request.form["title"],
            "date": request.form["date"],
            "location": request.form["location"],
            "category": request.form["category"]
        }
        data["events"].append(new_event)
        data["registrations"][str(new_id)] = []
        save_data(data)
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):
    data = load_data()
    event = next((e for e in data["events"] if e["id"] == event_id), None)

    if not event:
        return "Event not found", 404

    if request.method == "POST":
        user = request.form["name"].strip()
        reg_list = data["registrations"].get(str(event_id), [])

        if user and user not in reg_list:
            reg_list.append(user)
            data["registrations"][str(event_id)] = reg_list
            save_data(data)  # Save changes to file

        return redirect(url_for("home"))

    return render_template("register.html", event=event)

if __name__ == "__main__":
    app.run(debug=True)

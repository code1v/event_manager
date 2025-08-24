from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary event storage
events = [
    {"id": 1, "title": "Hackathon 2025", "date": "2025-09-15", "location": "Auditorium", "category": "Tech"},
    {"id": 2, "title": "Cultural Fest", "date": "2025-10-01", "location": "Main Ground", "category": "Cultural"},
    {"id": 3, "title": "Sports Meet", "date": "2025-09-20", "location": "Sports Complex", "category": "Sports"},
]

# Store registrations like: { event_id: [names] }
registrations = {1: [], 2: [], 3: []}


@app.route("/")
def home():
    # Pass both events and their registrations to template
    return render_template("index.html", events=events, registrations=registrations)


@app.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        new_id = len(events) + 1
        new_event = {
            "id": new_id,
            "title": request.form["title"],
            "date": request.form["date"],
            "location": request.form["location"],
            "category": request.form["category"]
        }
        events.append(new_event)
        registrations[new_id] = []  # also add new key in registrations
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        return "Event not found", 404

    if request.method == "POST":
        user = request.form["name"].strip()
        if user and user not in registrations[event_id]:
            registrations[event_id].append(user)  # add student name
        return redirect(url_for("home"))

    return render_template("register.html", event=event)


if __name__ == "__main__":
    app.run(debug=True)

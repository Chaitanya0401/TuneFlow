from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this for production

import json

# Load song data from JSON
with open("data/2025a1.json", "r") as file:
    data = json.load(file)
    songs_data = data["songs"]

# Mock user database (to be replaced with DynamoDB)
users = {
    "s40192780@student.rmit.edu.au": {"username": "JohnDoe0", "password": "012345"},
    "s40192781@student.rmit.edu.au": {"username": "JohnDoe1", "password": "123456"},
    "s40192782@student.rmit.edu.au": {"username": "JohnDoe2", "password": "234567"},
    "s40192783@student.rmit.edu.au": {"username": "JohnDoe3", "password": "345678"},
    "s40192784@student.rmit.edu.au": {"username": "JohnDoe4", "password": "456789"},
    "s40192785@student.rmit.edu.au": {"username": "JohnDoe5", "password": "567890"},
    "s40192786@student.rmit.edu.au": {"username": "JohnDoe6", "password": "678901"},
    "s40192787@student.rmit.edu.au": {"username": "JohnDoe7", "password": "789012"},
    "s40192788@student.rmit.edu.au": {"username": "JohnDoe8", "password": "890123"},
    "s40192789@student.rmit.edu.au": {"username": "JohnDoe9", "password": "901234"}
}


# Load music data from JSON (to be replaced with DynamoDB)
with open("data/2025a1.json", "r") as file:
    music_db = json.load(file)["songs"]

# Mock user subscriptions (to be replaced with DynamoDB)
subscriptions = {}

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email in users and users[email]["password"] == password:
            session["email"] = email
            session["username"] = users[email]["username"]
            return redirect(url_for("main_page"))
        else:
            flash("Email or password is invalid", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        
        if email in users:
            flash("The email already exists", "danger")
        else:
            users[email] = {"username": username, "password": password}
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/main", methods=["GET", "POST"])
def main_page():
    if "email" not in session:
        return redirect(url_for("login"))
    
    user_email = session["email"]
    user_subs = subscriptions.get(user_email, [])
    
    if request.method == "POST":
        search_title = request.form.get("title")
        search_artist = request.form.get("artist")
        search_year = request.form.get("year")
        search_album = request.form.get("album")
        
        results = [
            song for song in music_db 
            if (not search_title or search_title.lower() in song["title"].lower()) and
               (not search_artist or search_artist.lower() in song["artist"].lower()) and
               (not search_year or search_year == song["year"]) and
               (not search_album or search_album.lower() in song["album"].lower())
        ]
        
        if not results:
            flash("No result is retrieved. Please query again", "warning")
    
        return render_template("main.html", username=session["username"], user_subs=user_subs, search_results=results)
    
    return render_template("main.html", username=session["username"], user_subs=user_subs, search_results=[])

@app.route("/subscribe/<title>")
def subscribe(title):
    if "email" not in session:
        return redirect(url_for("login"))

    user_email = session["email"]
    song = next((s for s in music_db if s["title"] == title), None)

    if song and user_email in subscriptions:
        subscriptions[user_email].append(song)
    elif song:
        subscriptions[user_email] = [song]

    return redirect(url_for("main_page"))

@app.route("/remove/<title>")
def remove_subscription(title):
    if "email" not in session:
        return redirect(url_for("login"))

    user_email = session["email"]
    if user_email in subscriptions:
        subscriptions[user_email] = [s for s in subscriptions[user_email] if s["title"] != title]

    return redirect(url_for("main_page"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/query", methods=["POST"])
def query():
    if "username" not in session:
        return redirect(url_for("login"))

    # Dummy user subscriptions (replace with actual DynamoDB query later)
    user_subs = session.get("user_subs", [])  # Retrieve user subscriptions from session

    title = request.form.get("title", "").strip().lower()
    artist = request.form.get("artist", "").strip().lower()
    album = request.form.get("album", "").strip().lower()
    year = request.form.get("year", "").strip()

    # Filter songs based on query parameters
    filtered_songs = []
    for song in songs_data:  # Now this will be defined
        if (not title or title in song["title"].lower()) and \
           (not artist or artist in song["artist"].lower()) and \
           (not album or album in song["album"].lower()) and \
           (not year or year == song["year"]):
            filtered_songs.append(song)

    return render_template("main.html", username=session["username"], user_subs=user_subs, search_results=filtered_songs)


if __name__ == "__main__":
    app.run(debug=True, port = 65745)

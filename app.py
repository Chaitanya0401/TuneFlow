from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
import boto3


app = Flask(__name__)
app.secret_key = "cc-lab1"


# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # Change region as needed

# Reference the login table and music table
login_table = dynamodb.Table("Login")  # Your table name
music_table = dynamodb.Table("music")


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

from flask import Flask, render_template, request, redirect, url_for, session




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Query DynamoDB
        response = login_table.get_item(Key={"email": email})
        user = response.get("Item")

        if user and user["password"] == password:
            session["username"] = user["username"]  # Store username in session
            
            print("✅ Login successful! Redirecting to main page...")  # Debug
            print("Session Data:", session)  # Print session
            
            return redirect(url_for("main_page"))  # Redirect to main page
        else:
            return render_template("login.html", error="Email or password is invalid")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        response = login_table.get_item(Key={"email": email})
        if "Item" in response:
            return render_template("register.html", error="The email already exists")

        # Add new user to DynamoDB
        login_table.put_item(Item={"email": email, "username": username, "password": password})
        
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/main", methods=["GET"])
def main_page():
    if "username" not in session:
        return redirect(url_for("login"))

    # Fetch all music data from DynamoDB
    response = music_table.scan()
    all_songs = response.get("Items", [])

    return render_template("main.html", username=session["username"], songs=all_songs)

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
    title = request.form.get("title", "").strip()
    artist = request.form.get("artist", "").strip()
    yr = request.form.get("year", "").strip()
    album = request.form.get("album", "").strip()

    # Build filter conditions
    filter_expression = []
    expression_values = {}
    expression_names = {}  # Needed for reserved keywords like "year"

    if title:
        filter_expression.append("title = :title")
        expression_values[":title"] = title
    if artist:
        filter_expression.append("artist = :artist")
        expression_values[":artist"] = artist
    if yr:
        filter_expression.append("#yr = :year")  # Use alias #yr instead of "year"
        expression_values[":year"] = int(yr)
        print("input year:", yr)  # Debug
        expression_names["#yr"] = "year"
    if album:
        filter_expression.append("album = :album")
        expression_values[":album"] = album

    # Construct the filter expression
    if filter_expression:
        filter_string = " AND ".join(filter_expression)
        scan_params = {
            "FilterExpression": filter_string,
            "ExpressionAttributeValues": expression_values,
        }
        
        # Include ExpressionAttributeNames if "year" was used
        if expression_names:
            scan_params["ExpressionAttributeNames"] = expression_names
            print("ExpressionAttributeNames:", scan_params["ExpressionAttributeNames"])  # Debug

        response = music_table.scan(**scan_params)
        search_results = response.get("Items", [])
    else:
        search_results = []


    return render_template("main.html", search_results=search_results, username=session["username"])



if __name__ == "__main__":
    app.run(debug=True, port = 65745)

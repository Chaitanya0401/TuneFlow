from flask import Flask, render_template, request, redirect, url_for, session
import json
import boto3

app = Flask(__name__)
app.secret_key = "cc-lab1"

# DynamoDB resources
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
login_table = dynamodb.Table("login")
music_table = dynamodb.Table("music")
subscriptions_table = dynamodb.Table("Subscriptions")  # New subscriptions table

# Load music data (backup/fallback)
with open("data/2025a1.json", "r") as file:
    music_db = json.load(file)["songs"]


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        response = login_table.get_item(Key={"email": email})
        user = response.get("Item")

        if user and user["password"] == password:
            session["email"] = user["email"]
            session["username"] = user["username"]
            return redirect(url_for("main_page"))
        else:
            return render_template("login.html", error="Email or password is invalid")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        response = login_table.get_item(Key={"email": email})
        if "Item" in response:
            return render_template("register.html", error="The email already exists")

        login_table.put_item(Item={"email": email, "username": username, "password": password})
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/main", methods=["GET"])
def main_page():
    if "username" not in session or "email" not in session:
        return redirect(url_for("login"))

    # Fetch all music data
    all_songs = music_table.scan().get("Items", [])

    # Fetch subscriptions
    subs_response = subscriptions_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(session["email"])
    )
    user_subs = subs_response.get("Items", [])

    print(f"User's subscriptions: {user_subs}")  # Debugging line

    return render_template("main.html", username=session["username"], songs=all_songs, subscriptions=user_subs)



@app.route("/subscribe/<title>", methods=["GET", "POST"])
def subscribe(title):
    if "email" not in session:
        return redirect(url_for("login"))

    user_email = session["email"]
    song = next((s for s in music_db if s["title"] == title), None)

    if song:
        # Check if already subscribed
        response = subscriptions_table.get_item(Key={"email": user_email, "title": title})
        if "Item" not in response:
            subscriptions_table.put_item(Item={
                "email": user_email,
                "title": title,
                "artist": song["artist"],
                "album": song["album"],
                "year": song["year"]
            })
            print(f"Subscription added for {user_email} to song: {title}")  # Debugging line

    return redirect(url_for("main_page"))


@app.route("/remove/<title>", methods=["POST"])
def unsubscribe(title):
    if "email" not in session:
        return redirect(url_for("login"))

    user_email = session["email"]
    
    # Delete the subscription item from DynamoDB
    subscriptions_table.delete_item(Key={
        "email": user_email,
        "title": title
    })

    return redirect(url_for("main_page"))




@app.route("/query", methods=["POST"])
def query():
    title = request.form.get("title", "").strip()
    artist = request.form.get("artist", "").strip()
    yr = request.form.get("year", "").strip()
    album = request.form.get("album", "").strip()

    filter_expression = []
    expression_values = {}
    expression_names = {}

    if title:
        filter_expression.append("title = :title")
        expression_values[":title"] = title
    if artist:
        filter_expression.append("artist = :artist")
        expression_values[":artist"] = artist
    if yr:
        filter_expression.append("#yr = :year")
        expression_values[":year"] = int(yr)
        expression_names["#yr"] = "year"
    if album:
        filter_expression.append("album = :album")
        expression_values[":album"] = album

    if filter_expression:
        scan_params = {
            "FilterExpression": " AND ".join(filter_expression),
            "ExpressionAttributeValues": expression_values
        }

        if expression_names:
            scan_params["ExpressionAttributeNames"] = expression_names

        response = music_table.scan(**scan_params)
        search_results = response.get("Items", [])
    else:
        search_results = []

    return render_template("main.html", username=session["username"],
                           songs=[],  # Only show search results
                           subscribed_music=[],
                           search_results=search_results)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=65745)

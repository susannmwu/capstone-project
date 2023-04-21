from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, NationalParks, Trail

from jinja2 import StrictUndefined
import os
import requests
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["NPS_KEY"]


@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/national-parks")
def all_national_parks():
    """View all National Parks"""
    national_parks = crud.get_national_parks()

    return render_template("all_national_parks.html",
                           national_parks=national_parks)


@app.route("/national-parks/<np_id>")
def show_national_park(np_id):
    """Show details about a particular national park."""

    national_park = crud.get_np_by_id(np_id)

    return render_template("national_park_details.html", national_park=national_park)


@app.route("/national-parks/trails")
def find_trails():
    """Search for National Parks trails using NPS thingstodo endroute"""
    parkCode = request.args.get("parkCode", "")
    q = request.args.get("q", "")
    sort = request.args.get("sort", "")

    things_to_do_url = "https://developer.nps.gov/api/v1/thingstodo"
    places_url = "https://developer.nps.gov/api/v1/places"

    payload = {"api_key": API_KEY,
               "parkCode": parkCode,
               "limit": "500"}

    res = requests.get(things_to_do_url, params=payload)
    response = requests.get(places_url, params=payload)

    # keys are dict_keys(['total', 'limit', 'start', 'data'])
    res_json = res.json()
    response_json = response.json()

    res_json_list = res_json["data"]
    response_json_list = response_json["data"]

    hiking_trails = []

    for item in res_json_list:
        activities = item["activities"]
        for activity in activities:
            if activity["name"] == "Hiking":
                hiking_trails.append(item["title"])
                print(hiking_trails)

    for item in response_json_list:
        amenities = item["amenities"]
        for amenity in amenities:
            if amenity == "Trailhead":
                hiking_trails.append(item["title"])
                print(hiking_trails)

    #     # res_json["data"] is a list and I need to figure out how to parse the data out
    #     # in each item of the list, there's a key called activities

    return render_template("trails-search-results.html",
                           data=res_json,
                           hiking_trails=hiking_trails)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

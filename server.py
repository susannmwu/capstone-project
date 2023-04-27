from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db

from jinja2 import StrictUndefined
import os
import requests
import crud
import re
import model

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["NPS_KEY"]


@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")


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


@app.route("/logout")
def logout():
    """Log users out"""
    del session["user_email"]
    session.clear()
    flash("You've logged out successfully.")
    return redirect("/")


@app.route("/national-parks/trails")
def find_trails():
    """Search for National Parks trails using NPS thingstodo and places endroute"""

    parkCode = request.args.get("parkCode", "")

    things_to_do_url = "https://developer.nps.gov/api/v1/thingstodo"
    places_url = "https://developer.nps.gov/api/v1/places"

    payload = {"api_key": API_KEY,
               "parkCode": parkCode,
               "limit": "500"}

    res = requests.get(things_to_do_url, params=payload)
    response = requests.get(places_url, params=payload)

    res_json = res.json()
    response_json = response.json()

    res_json_list = res_json["data"]
    response_json_list = response_json["data"]

    hiking_trails = []

    for item in res_json_list:
        activities = item["activities"]
        images = item["images"]
        for activity in activities:
            if activity["name"] == "Hiking":
                item["longDescription"] = re.sub(
                    r"<.*?>", "", item["longDescription"])
                for image in images:
                    url = image["url"]
                hiking_trails.append(
                    {"name": item["title"], "description": item["longDescription"], "images": url})

    for item in response_json_list:
        amenities = item["amenities"]
        images = item["images"]
        for amenity in amenities:
            if amenity == "Trailhead":
                item["bodyText"] = re.sub(r"<.*?>", "", item["bodyText"])
                for image in images:
                    url = image["url"]
                hiking_trails.append(
                    {"name": item["title"], "description": item["bodyText"], "images": url})

    return render_template("trails-search-results.html",
                           data=res_json,
                           parkCode=parkCode,
                           hiking_trails=hiking_trails)


@app.route("/national-parks/<np_id>/favorite-parks", methods=["POST"])
def add_favorite_park(np_id):
    """Add park to user's favorites"""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to add a park to your favorite parks list")
    else:
        user = crud.get_user_by_email(logged_in_email)
        national_park = crud.get_np_by_id(np_id)

        # create a favorite park object
        fav_park = crud.create_fav_park(user, national_park)

        flash(
            f"You've added this {national_park.np_name} to your favorite parks list")

    return render_template("user_details.html", user=user)


# @app.route("/national-parks/<np_id>/update-fav-parks", methods=["POST"])
# def update_favorite_park():
#     """Allow a user to update favorite parks list"""
#     np_id = request.json["favorite_park_id"]


@app.route("/national-parks/trails/<trail_name>", methods=["POST"])
def add_favorite_trail(trail_name):
    """Add trail to user's favorites"""

    trail_description = request.args.get("description")
    parkcode = request.args.get("parkcode")

    logged_in_email = session.get("user_email")

    user = crud.get_user_by_email(logged_in_email)
    user_fav_trails = crud.get_user_fav_trail(logged_in_email)
    parkcode = crud.get_np_by_parkcode(parkcode)
    np_id = crud.get_np_by_id(parkcode)

    if logged_in_email is None:
        flash("You must log in to add a trail to your favorite trails list")

    elif parkcode in user_fav_trails:

        flash(f"You've added this trail to your favorites trail list")

    else:
        new_fav_trail = crud.create_fav_trail(
            user, np_id, trail_name, trail_description)

        db.session.add(new_fav_trail)
        db.session.commit()

    # query db for favorite trails with user and trail name and parkcode
    # if there's a match -> "you've already added this trail"

    # create a crud function to query national_park from parkcode
    # if not create a new favorite trail
    # need to get np_id

    return render_template("user_details.html", user=user, trail_description=trail_description)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

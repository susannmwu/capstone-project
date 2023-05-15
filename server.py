from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db, FavoritePark, NationalParks
# from passlib.hash import argon2

from jinja2 import StrictUndefined
import os
import requests
import crud
import re

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

    park_code = national_park.park_code
    np_images = crud.get_np_images(park_code)
    # print(np_images)
    return render_template("national_park_details.html", national_park=national_park, np_images=np_images)


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/user_profile")
def show_user_profile():
    """View user individual profile"""

    if "user_email" in session:
        logged_in_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_email)
        user_id = user.user_id
        return redirect(f"/users/{user_id}")
    else:
        flash("Please log in to view user profile")
        return ("/")


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
    """Add park to user's favorite parks list"""

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    national_park = crud.get_np_by_id(np_id)
    user_fav_parks = user.favorite_parks

    if logged_in_email is None:
        flash("You must log in to add a park to your favorite parks list")

    # if np_id already exists in the user's favorite park list, then flash the message
    elif national_park in user_fav_parks:
        flash(
            f" '{national_park.np_name}' already exists in your favorite parks list")

    # otherwise, create a new park and flash the message
    else:
        fav_park = crud.create_fav_park(user, national_park)

        flash(
            f"Success! Added '{national_park.np_name}' to your favorite parks list")

    return render_template("user_details.html", user=user)


@app.route("/remove-fav-park", methods=["POST"])
def remove_favorite_park():
    """Remove park from user's favorite parks list"""

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    park_to_remove = request.form.get("remove_park")

    if logged_in_email is None:
        flash("You must log in to remove a park to your favorite parks list")
    else:
        park_removal = crud.find_park_to_remove(user, park_to_remove)

        db.session.delete(park_removal)
        db.session.commit()

        flash(f"'{park_to_remove}' was removed from your favorites list")

    return render_template("user_details.html", user=user, park_to_remove=park_to_remove)


@app.route("/national-parks/trails/<trail_name>", methods=["POST"])
def add_favorite_trail(trail_name):
    """Add trail to user's favorites"""

    # grabbing the following information from html form
    trail_description = request.form.get("description")
    parkcode = request.form.get("parkcode")

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)

    national_park = crud.get_np_by_parkcode(parkcode)

    # getting all users favorite trails
    user_fav_trails = crud.get_all_users_fav_trails(logged_in_email)

    if logged_in_email is None:
        flash("You must log in to add a trail to your favorite trails list")

    # need to double check syntax for line 248
    elif trail_name in user_fav_trails:
        flash(f"'{trail_name}' already exists in your favorite trails list")

    else:
        new_fav_trail = crud.create_fav_trail(
            user, national_park.np_id, trail_name, trail_description)

        db.session.add(new_fav_trail)
        db.session.commit()
        flash(
            f"Success! Added '{trail_name}' trail to your favorites trail list")

    # query db for favorite trails with user and trail name and parkcode
    # if there's a match -> "you've already added this trail"

    # create a crud function to query national_park from parkcode
    # if not create a new favorite trail
    # need to get np_id

    return render_template("user_details.html", user=user, trail_description=trail_description)


@app.route("/np-entry.json", methods=["POST"])
def add_park_entry():
    np = request.json.get("np_name")
    park_entry = request.json.get("park_entries")

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)

    if logged_in_email is None:
        flash("You must log in to add a memory of your favorite parks")
    else:
        new_park_entry = crud.create_park_entry(user, np, park_entry)
        db.session.add(new_park_entry)
        db.session.commit()
        flash(f"Sucess! You've added a park memory")

    return jsonify({"np": np, "entry": park_entry})


# @app.route("/remove-park.json", methods=["POST"])
# def remove_park():
#     remove_park = request.json.get("remove_park")
#     # print(remove_park)

#     logged_in_email = session.get("user_email")
#     user = crud.get_user_by_email(logged_in_email)
#     # print(user)
#     if not user:
#         flash("You must log in to remove a park from your list")
#     else:
#         # park_object = NationalParks.query.filter(
#         #     NationalParks.np_name == remove_park).first()
#         # print(park_object)
#         # park_to_remove = FavoritePark.query.filter(
#         #     FavoritePark.user_id == user.user_id, FavoritePark.np_id == park_object.np_id).first()
#         # print(park_to_remove)
#         # # park_removal = crud.remove_fav_park(remove_park)
#         # db.session.delete(park_to_remove)
#         # db.session.commit()
#         # flash(f"Sucess! You've removed a favorited park from your list")

#         park_removal = crud.find_park_to_remove(user, remove_park)

#         db.session.delete(park_removal)
#         db.session.commit()
#         flash(
#             f"Sucess! You've removed '{remove_park}' from your list")
#     return jsonify({"np": remove_park})


# @app.route("/remove-park-entry.json", methods=["POST"])
# def remove_park_entry():
#     remove_np_name = request.json.get("")
#     remove_park_entry = request.json.get("")

#     logged_in_email = session.get("user_email")
#     user = crud.get_user_by_email(logged_in_email)

#     if not user:
#         flash("You must log in to remove a park entry from your list")

#     else:
#         park_entry_removal = crud.find_park_entry_to_remove(
#             user, remove_park_entry)
#         db.session.delete(park_entry_removal)
#         db.session.commit()
#         flash(f"Sucess! You've removed a park entry")
#     return jsonify({"np"})


@app.route("/api/map")
def map_info():
    """JSON information about national park latitude and longitude"""

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)

    coordinates = []

    user_fav_parks = user.favorite_parks

    for park in user_fav_parks:
        lat = float(park.latitude)
        long = float(park.longitude)
        np_name = park.np_name
        coordinates.append(
            {"np": np_name,
             "latitude": lat,
             "longitude": long})

    return jsonify(coordinates)


@app.route("/search-park", methods=["POST"])
def search_all_parks():
    """Search for national parks and be redirected to national parks details page"""
    np_name = request.form.get("search")

    # print("############")
    # print(np_name)

    np_id = crud.get_np_id_by_np_name(np_name)

    return redirect(f"/national-parks/{np_id}")


@app.route("/nps-tweets")
def nps_tweets():
    """View NPS tweets """

    return render_template("nps_tweets.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

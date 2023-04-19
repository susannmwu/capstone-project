from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, NationalParks, Trail

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")


@app.route("/national-parks")
def all_national_parks():
    """View all National Parks"""
    national_park = NationalParks.all_national_parks()

    return render_template("all_national_parks.html", national_park=national_park)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

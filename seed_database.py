"""Script to seed database."""
from flask import Flask, request
from pprint import pformat
import os
import requests


import os
import crud
import model
import server

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

os.system("dropdb trails")
os.system("createdb trails")
model.connect_to_db(server.app)
model.db.create_all()


"""Search for national parks info"""
# https://developer.nps.gov/api/v1/parks?api_key=

API_KEY = os.environ["NPS_KEY"]

payload = {"api_key": API_KEY}
payload["limit"] = "500"

url = "https://developer.nps.gov/api/v1/parks"
res = requests.get(url, params=payload)

# dictionary of query
res_json = res.json()

# list of query
parks_list = res_json["data"]

park_designations = ["National and State Parks",
                     "National Park & Preserve", "National Park", "National Parks"]

# 61 parks, could not get American Samoa

national_parks = []

for park in parks_list:
    if park["designation"] in park_designations:
        national_parks.append(park)

# print(national_parks[0])
for park in national_parks:
    parkcode = park.get("parkCode")
    fullname = park.get("fullName")
    description = park.get("description")
    image_url = park["images"][0]["url"]
    # print(f"{fullname}")
    # print(f"{image_url}")
    np = crud.create_national_parks(parkcode, fullname, description, image_url)
    model.db.session.add(np)

model.db.session.commit()


########################################################################
susan = crud.create_user("Susan", "Wu", "susanwu@gmail.com", "cats")
model.db.session.add(susan)
model.db.session.commit()

yosemite = model.NationalParks.query.filter(
    model.NationalParks.np_name == "Yosemite National Park").first()

fav_park = model.FavoritePark(
    user_id=susan.user_id, np_id=yosemite.np_id)

model.db.session.add(fav_park)
model.db.session.commit()

# cloudsrest = model.FavoriteTrail.query.filter(model.Trail.trail_name)
# fav_trail = model.FavoriteTrail(
#     user_id=susan.user_id, trail_id=cloudsrest.trail_id)

# model.db.session.add(fav_trail)
# model.db.session.commit()

# # Create a NP
# yosemite = crud.create_national_parks("Yosemite National Park",
#                                       "The geology of the Yosemite area is characterized by granite rocks and remnants of older rock.",
#                                       "hiking")

# model.db.session.add(yosemite)
# model.db.session.commit()

# # Create a trail
# clouds_rest = crud.create_np_trails("Clouds Rest", "Cloud's Rest, a massive granite formation just northeast of Half Dome in Yosemite Valley, is famous for its very high degree of visual prominence in the valley as well as its razor-sharp ridge near the summit.",
#                                     "Out & back", 12.2, "strenuous")
# model.db.session.add(clouds_rest)
# model.db.session.commit()

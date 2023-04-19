"""Script to seed database."""
from flask import Flask, request
from pprint import pformat
import os
import requests


import os
import json
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

########################################################################

"""Search for national parks info"""
# https://developer.nps.gov/api/v1/parks?api_key=
# API_KEY = os.environ["NPS_KEY"]

# payload = {"api_key": API_KEY}
url = "https://developer.nps.gov/api/v1/parks?limit=468&start=0&api_key=O8FJvg81PaGUCA8plmVfUnC9zuvg7lEcGbdjmIQI"
res = requests.get(url)

# dictionary of query
res_json = res.json()

# list of query
parks_list = res_json["data"]

# for result in parks_list:
#     fullname = result.get("fullName")
#     parkcode = result. get("parkCode")
#     description = result.get("description")
#     print(f"{fullname}")

park_designations = ["National and State Parks",
                     "National Park & Preserve", "National Park", "National Parks"]
national_parks = []

for park in parks_list:
    if park["designation"] in park_designations:
        national_parks.append(park)

# 61 parks, could not get American Samoa
# print(len(national_parks))

for park in national_parks:
    parkcode = park.get("parkCode")
    fullname = park.get("fullName")
    description = park.get("description")
    # print(f"{parkcode} {fullname}")

    np = crud.create_national_parks(parkcode, fullname, description)
    model.db.session.add(np)

    model.db.session.commit()


########################################################################
# odds = crud.create_user("Odds", "Cat", "Cat@cat.com", "MoarFoodPls")
# model.db.session.add(odds)
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

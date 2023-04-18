"""Script to seed database."""

import os
import json
import crud
import model
import server

os.system("dropdb trails")
os.system("createdb trails")
model.connect_to_db(server.app)
model.db.create_all()

# Load trail data from JSON file
# with open("/data/trails.json") as f:
#     trail_data = json.loads(f.read())


# Create 10 users; each user will make 10

# for n in range(10):
#     email = f"user{n}@test.com"
#     password = "test"

#     user = crud.create_user(email, password)
#     model.db.session.add(user)

odds = crud.create_user("Odds", "Cat", "Cat@cat.com", "MoarFoodPls")
model.db.session.add(odds)
model.db.session.commit()

# Create a NP
yosemite = crud.create_national_parks("Yosemite National Park",
                                      "The geology of the Yosemite area is characterized by granite rocks and remnants of older rock.",
                                      "hiking")

model.db.session.add(yosemite)
model.db.session.commit()

# Create a trail
clouds_rest = crud.create_np_trails("Clouds Rest", "Cloud's Rest, a massive granite formation just northeast of Half Dome in Yosemite Valley, is famous for its very high degree of visual prominence in the valley as well as its razor-sharp ridge near the summit.",
                                    "Out & back", 12.2, "strenuous")
model.db.session.add(clouds_rest)
model.db.session.commit()

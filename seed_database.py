"""Script to seed database."""

import os
import json
import crud
import model
import server

os.system
os.sytem("createdb trails")
model.connect_to_db(server.app)
model.db.create_all()

# Load trail data from JSON file
with open("/data/trails.json") as f:
    trail_data = json.loads(f.read())


# Create 10 users; each user will make 10

for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

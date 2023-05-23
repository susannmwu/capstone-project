# Happy Trails

Happy Trails is a web app built using Python and Javascript that allows users to search for hiking trails at national parks.

Users can save parks, hiking trails and park memories to their dashboard. Happy Trails is a web app created by Susan Wu. Susan is passionate about national parks and the outdoors and hopes to one day complete her bucket list of visiting all 63 US national parks!

<img width="1436" alt="Happy Trails" src="https://github.com/susannmwu/capstone-project/assets/127285836/384f9f43-d65f-46ce-9d37-a9bdcb65792a">

## Table of Contents

- Technologies used

- How to locally run app

- Features

## Technologies Used

- Python

- JavaScript

- AJAX/JSON

- Flask

- PostgresSQL

- SQLAlchemy

- Jinja2

- Bootstrap

- Google Maps API

- National Park Service API

(dependencies are listed in requirements.txt)

## How to locally run Happy Trails

Happy Trails has not yet been deployed, so here is how you can run the app locally on your machine.

- Obtain an API Key from the National Park Service API and add to: `secrets.sh`

- Set up and activate a Python virtualenv and install all dependencies:

- `pip install -r requirements.txt`

- Create a new database in psql named trails:

- `psql`

- `createdb trails;`

- Create the tables in your database:

- `python3 model.py`

- Seed database:

- `python3 seed_database.py`

- Start up the Flask server:

- `python3 server.py`

- Go to localhost:5000 on your web browser

## Features

- #### View all national parks

https://github.com/susannmwu/capstone-project/assets/127285836/7a242cc2-9035-4fa3-ba3e-a1131f38bca3

- #### View park details & save parks

https://github.com/susannmwu/capstone-project/assets/127285836/db29a087-7761-4f4b-ac48-0d9cb610ee80

- #### Search & save hiking trails

https://github.com/susannmwu/capstone-project/assets/127285836/cc40f057-49d3-4424-865a-b4abea9debf9

- #### Save park memories on user dashboard

https://github.com/susannmwu/capstone-project/assets/127285836/673abb00-bb74-4d9e-9e97-07f7c0dfc089

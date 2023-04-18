"""CRUD operations"""

from model import db, User, NationalParks, Trail, FavoritePark, FavoriteTrail, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(first_name, last_name, email, password):
    """Create and return a new user."""
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password)
    return user


def get_user_by_id(user_id):
    """Return a user by primary key"""

    return User.query.get(user_id)


def create_national_parks(np_name, overview, things_to_do):
    """Create a National Park."""

    np = NationalParks(np_name=np_name,
                       overview=overview,
                       things_to_do=things_to_do)

    return np


def create_trails(trail_name, trail_description, trail_type, trail_length, trail_difficulty):
    """Create a NP trail."""

    trail = Trail(trail_name=trail_name,
                  trail_description=trail_description,
                  trail_type=trail_type,
                  trail_length=trail_length,
                  trail_difficulty=trail_difficulty)

    return trail


def get_national_parks():
    """Return all national parks"""

    return NationalParks.query.all()


def get_national_park_by_id(np_id):
    """Return national parks by id."""

    return NationalParks.query.get(np_id)


def get_trails():
    """Return all trails"""

    return Trail.query.all()


def get_user_favorite_parks():

    return

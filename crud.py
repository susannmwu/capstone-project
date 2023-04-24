"""CRUD operations"""

from model import db, User, NationalParks, Trail, FavoritePark, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(first_name, last_name, email, password):
    """Create and return a new user."""
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password)
    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_national_parks(park_code, np_name, description, image_url):
    """Create a National Park."""

    np = NationalParks(park_code=park_code,
                       np_name=np_name,
                       description=description,
                       image_url=image_url)

    return np


def get_national_parks():
    """Return all national parks"""

    return NationalParks.query.all()


def get_np_by_id(np_id):
    """Return national parks by np_id"""
    NationalParks.query.get(np_id)

    return NationalParks.query.get(np_id)


def create_fav_park(user, national_park):
    """Create and return a park for user's favorite parks"""

    fav_park = FavoritePark(user_id=user.user_id, np_id=national_park.np_id)
    db.session.add(fav_park)
    db.session.commit()
    return fav_park


def get_user_fav_park(user_id):
    """Returns a list of user's favorite parks"""

    user_fav_parks = FavoritePark.query.filter(User.user_id == user_id).first()

    user_fav_parks_lst = []

    for park in user_fav_parks:
        user_fav_parks_lst.append(park)

    return user_fav_parks_lst

################################################################################
# def create_np_trails(trail_name, trail_description, trail_type, trail_length, trail_difficulty):
#     """Create a NP trail."""

#     trail = Trail(trail_name=trail_name,
#                   trail_description=trail_description,
#                   trail_type=trail_type,
#                   trail_length=trail_length,
#                   trail_difficulty=trail_difficulty)

#     return trail


# def get_trails():
#     """Return all trails"""

#     return Trail.query.all()

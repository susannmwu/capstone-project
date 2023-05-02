"""CRUD operations"""

from model import db, User, NationalParks, FavoritePark, FavoriteTrail, connect_to_db

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


def create_national_parks(park_code, np_name, latitude, longitude, description, image_url):
    """Create a National Park."""

    np = NationalParks(park_code=park_code,
                       np_name=np_name,
                       latitude=latitude,
                       longitude=longitude,
                       description=description,
                       image_url=image_url)

    return np


def get_national_parks():
    """Return all national parks"""

    return NationalParks.query.all()


def get_np_by_id(np_id):
    """Return national parks by np_id"""

    return NationalParks.query.get(np_id)


def get_np_by_parkcode(park_code):
    # find np where parkcode == parkcode
    """Return national park by parkcode"""
    return NationalParks.query.filter(park_code == park_code).first()


def create_fav_park(user, national_park):
    """Create and return a park as user's favorite parks"""

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


def remove_fav_park(user_id, np_id):
    np_id = NationalParks.query.get(np_id)
    user = User.query.get(user_id)
    user_fav_park = user.favorite_parks

    for park in user_fav_park:
        if park.np_id == np_id:
            park_removal = park.np_id
    return park_removal


def create_fav_trail(user, np_id, trail_name, trail_description):
    """Create and return a trail as user's favorite trail"""

    fav_trail = FavoriteTrail(user_id=user.user_id,
                              np_id=np_id,
                              trail_name=trail_name,
                              trail_description=trail_description)

    return fav_trail


def get_all_users_fav_trails(email):

    all_fav_trails = []
    user = User.query.filter(User.email == email).first()
    fav_trails = user.favorite_trails

    for trail in fav_trails:
        all_fav_trails.append(trail.trail_name)
    return all_fav_trails


# def create_park_entry(user):
#     park_entry = FavoritePark(user_id=user.user_id)

#     return park_entry

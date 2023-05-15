"""CRUD operations"""

from model import db, User, NationalParks, FavoritePark, FavoriteTrail, ParkEntry, ParkImage, connect_to_db

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


def get_all_user_emails():
    """Return a list of all user emails"""
    all_emails = []

    for user in User.query.all():
        user_email = user.email
        all_emails.append(user_email)
    return all_emails


def create_national_parks(park_code, np_name, latitude, longitude, description, image_url):
    """Create a National Park."""

    np = NationalParks(park_code=park_code,
                       np_name=np_name,
                       latitude=latitude,
                       longitude=longitude,
                       description=description,
                       image_url=image_url)

    return np


def create_park_images(park_code, image_url, image_caption):
    """Create national park images"""

    img = ParkImage(park_code=park_code, image_url=image_url,
                    image_caption=image_caption)

    return img


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


def get_np_id_by_np_name(np_name):
    """Return national park id by np_name"""
    np_name = NationalParks.query.filter(
        NationalParks.np_name == np_name).first()
    national_park_id = np_name.np_id
    return national_park_id


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


def find_park_to_remove(user, park_name):
    park = NationalParks.query.filter(
        NationalParks.np_name == park_name).first()
    park_to_remove = FavoritePark.query.filter(
        FavoritePark.user_id == user.user_id, FavoritePark.np_id == park.np_id).first()
    return park_to_remove


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


def create_park_entry(user, np, entry):
    """Create and return a park entry of user's favorite park"""

    park_entry = ParkEntry(user_id=user.user_id, np=np, entry=entry)

    return park_entry


def get_user_all_park_entries(email):

    all_entries = []
    user = User.query.filter(User.email == email).first()
    park_entries = user.user_entries

    for entry in park_entries:
        all_entries.append(entry)
    return all_entries


def get_np_images(parkcode):

    all_park_images = []
   # filter park images by parkcode
    images = ParkImage.query.filter(ParkImage.park_code == parkcode).all()

    for img in images:
        all_park_images.append(img.image_url)

    return all_park_images

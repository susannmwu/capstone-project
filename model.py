"""Models for hiking trail app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    favorite_parks = db.relationship(
        "NationalParks", secondary="favorite_parks", back_populates="user_fav_parks")
    favorite_trails = db.relationship(
        "FavoriteTrail", back_populates="user")
    user_entries = db.relationship("ParkEntry", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

# change NationalParks class name to NationalPark


class NationalParks(db.Model):
    """A National Park."""
    __tablename__ = "national_parks"

    np_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_code = db.Column(db.String, nullable=False)
    np_name = db.Column(db.String, unique=True)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    description = db.Column(db.String)
    image_url = db.Column(db.String)

    user_fav_parks = db.relationship(
        "User", secondary="favorite_parks", back_populates="favorite_parks")
    national_park_trails = db.relationship(
        "FavoriteTrail", back_populates="national_park")
    entries = db.relationship(
        "ParkEntry", back_populates="park_entry")
    images = db.relationship("ParkImage", back_populates="park")

    def __repr__(self):
        return f"<National_Park np_id={self.np_id} np_name={self.np_name}>"


class FavoritePark(db.Model):

    __tablename__ = "favorite_parks"

    favorite_park_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    np_id = db.Column(db.Integer, db.ForeignKey(
        "national_parks.np_id"))

    def __repr__(self):
        return f"<Favorite_Park np_id={self.np_id} user_id={self.user_id}>"


class FavoriteTrail(db.Model):
    __tablename__ = "favorite_trails"

    favorite_trail_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    np_id = db.Column(db.Integer, db.ForeignKey("national_parks.np_id"))
    trail_name = db.Column(db.String)
    trail_description = db.Column(db.String)

    national_park = db.relationship(
        "NationalParks", back_populates="national_park_trails")
    user = db.relationship("User", back_populates="favorite_trails")

    def __repr__(self):
        return f"<Favorite_Trail fav_trail_id={self.favorite_trail_id} trail_name={self.trail_name}>"


class ParkEntry(db.Model):
    __tablename__ = "park_entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    np_id = db.Column(db.Integer, db.ForeignKey("national_parks.np_id"))
    np = db.Column(db.String)
    entry = db.Column(db.Text)

    user = db.relationship("User", back_populates="user_entries")
    park_entry = db.relationship(
        "NationalParks", back_populates="entries")

    def __repr__(self):
        return f"<Entry entry_id={self.entry_id}>"


class ParkImage(db.Model):

    __tablename__ = "park_image"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    np_id = db.Column(db.Integer, db.ForeignKey("national_parks.np_id"))
    park_code = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    image_caption = db.Column(db.String)

    park = db.relationship("NationalParks", back_populates="images")

    def __repr__(self):
        return f"<Park Images np_id={self.np_id} img_url_1={self.image_url}>"

    ##############################################################################
    # Helper functions


def connect_to_db(flask_app, db_uri="postgresql:///trails", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

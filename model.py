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

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

# change NationalParks class name to NationalPark


class NationalParks(db.Model):
    """A National Park."""
    __tablename__ = "national_parks"

    np_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_code = db.Column(db.String, nullable=False)
    np_name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    image_url = db.Column(db.String)

    user_fav_parks = db.relationship(
        "User", secondary="favorite_parks", back_populates="favorite_parks")
    national_park_trails = db.relationship(
        "FavoriteTrail", back_populates="national_park")

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
        return f"<Favorite_Park np_id={self.np_id} np_name={self.national_park}>"


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

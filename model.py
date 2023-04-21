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

    favorite_parks = db.relationship("FavoritePark", back_populates="user")
    favorite_trails = db.relationship("FavoriteTrail", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class NationalParks(db.Model):
    """A National Park."""
    __tablename__ = "national_parks"

    np_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_code = db.Column(db.String, nullable=False)
    np_name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    image_url = db.Column(db.String)

    favorite_parks = db.relationship(
        "FavoritePark", back_populates="national_park")
    national_park_trails = db.relationship(
        "Trail", back_populates="national_park")

    def __repr__(self):
        return f"<National_Park np_id={self.np_id} np_name={self.np_name}>"


class Trail(db.Model):
    """A National Park Trail."""
    __tablename__ = "trails"

    trail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    np_id = db.Column(db.Integer, db.ForeignKey("national_parks.np_id"))
    trail_name = db.Column(db.String)
    trail_description = db.Column(db.String)
    trail_type = db.Column(db.String)
    trail_length = db.Column(db.Integer)
    trail_difficulty = db.Column(db.String)

    favorite_trails = db.relationship("FavoriteTrail", back_populates="trail")
    national_park = db.relationship(
        "NationalParks", back_populates="national_park_trails")

    def __repr__(self):
        return f"<Trail trail_id={self.trail_id} trail_name={self.trail_name}>"


class FavoritePark(db.Model):
    __tablename__ = "favorite_parks"

    favorite_park_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    np_id = db.Column(db.Integer, db.ForeignKey(
        "national_parks.np_id"))
    np_reviews = db.Column(db.String)

    user = db.relationship("User", back_populates="favorite_parks")
    national_park = db.relationship(
        "NationalParks", back_populates="favorite_parks")

    def __repr__(self):
        return f"<Favorite_Park np_id={self.np_id} np_name={self.np_name}>"


class FavoriteTrail(db.Model):
    __tablename__ = "favorite_trails"

    favorite_trail_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"))
    trail_reviews = db.Column(db.String)

    user = db.relationship("User", back_populates="favorite_trails")
    trail = db.relationship("Trail", back_populates="favorite_trails")

    def __repr__(self):
        return f"<Favorite_Trail trail_id={self.trail_id} trail_name={self.trail_name}>"


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

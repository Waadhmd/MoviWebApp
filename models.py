from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(50))
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    poster_url = db.Column(db.String(250))
    # Add a unique constraint for the movie name
    __table_args__ = (db.UniqueConstraint('name'),)

    def __repr__(self):
        return f"<Movie {self.id}: {self.name}>"

    def __str__(self):
        return f"Movie {self.name} released in {self.year} "

class UserMovieStatus(db.Model):
    __tablename__ = 'user_movie_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'watched' or 'want-to-watch'
    watched_at = db.Column(db.DateTime, nullable=True) # To track streaks

    user = db.relationship('User', backref=db.backref('movie_statuses', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('user_statuses', lazy=True))

    def __repr__(self):
        return f"<UserMovieStatus {self.id}: User {self.user_id} Movie {self.movie_id} - {self.status}>"

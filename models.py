from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(50))
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(250))

    # foreign key to users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f"<Movie {self.id}: {self.name}>"

    def __str__(self):
        return f"Movie {self.name} released in {self.year} "


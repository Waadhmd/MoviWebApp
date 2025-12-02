from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Movie, UserMovieStatus
from datetime import datetime

class DataManager:
    """Handles CRUD operations for users, movies, and their statuses."""

    # User Operations
    def create_user(self, username: str, email: str, password: str) -> User:
        """Create and add a new user to the database."""
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    def find_user_by_username(self, username: str) -> User:
        """Find a user by their username."""
        return User.query.filter_by(username=username).first()

    def find_user_by_id(self, user_id: int) -> User:
        """Find a user by their id."""
        return User.query.get(user_id)

    def get_users(self):
        """Return all users from the database"""
        try:
            return User.query.all()
        except SQLAlchemyError as e :
            print(f"Error fetching users : {e}")
            return []

    # Movie Operations
    def get_movie_by_name(self, name: str) -> Movie:
        """Get a movie by its name."""
        return Movie.query.filter_by(name=name).first()

    def add_movie(self, name: str, director: str, year: int, poster_url: str, rating: float, user_id: int) -> Movie:
        """Add a movie to the database and associate it with a user."""
        try:
            movie = self.get_or_create_movie(name, director, year, poster_url, rating)
            
            status_entry = self.get_user_movie_status(user_id, movie.id)
            if not status_entry:
                self.set_user_movie_status(user_id, movie.id, 'want-to-watch')

            return movie
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding movie for user: {e}")
            return None

    def get_or_create_movie(self, name: str, director: str, year: int, poster_url: str, rating: float) -> Movie:
        """Get a movie by its name, or create it if it doesn't exist."""
        movie = self.get_movie_by_name(name)
        if not movie:
            movie = Movie(name=name, director=director, year=year, poster_url=poster_url, rating=rating)
            db.session.add(movie)
            db.session.commit()
        return movie

    def get_movies(self) -> list[Movie]:
        """Return all movies from the database"""
        try:
            return Movie.query.all()
        except SQLAlchemyError as e:
            print(f"Error fetching movies: {e}")
            return []

    def get_all_movies(self) -> list[Movie]:
        """Return all movies from the database without duplicates."""
        try:
            return Movie.query.group_by(Movie.id).all()
        except SQLAlchemyError as e:
            print(f"Error fetching all movies: {e}")
            return []

    # UserMovieStatus Operations
    def get_user_movie_status(self, user_id: int, movie_id: int) -> UserMovieStatus:
        """Get the status of a movie for a specific user."""
        return UserMovieStatus.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    def set_user_movie_status(self, user_id: int, movie_id: int, status: str) -> UserMovieStatus:
        """Set or update the status of a movie for a user."""
        try:
            status_entry = self.get_user_movie_status(user_id, movie_id)
            if status_entry:
                status_entry.status = status
                if status == 'watched':
                    status_entry.watched_at = datetime.utcnow()
            else:
                status_entry = UserMovieStatus(user_id=user_id, movie_id=movie_id, status=status)
                if status == 'watched':
                    status_entry.watched_at = datetime.utcnow()
                db.session.add(status_entry)
            db.session.commit()
            return status_entry
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error setting movie status: {e}")
            return None

    def get_user_movies_with_status(self, user_id: int):
        """Get all movies for a user with their watch status."""
        movies = db.session.query(Movie, UserMovieStatus.status).\
            join(UserMovieStatus, (UserMovieStatus.movie_id == Movie.id) & (UserMovieStatus.user_id == user_id)).\
            all()
        return movies

    def get_user_movies_by_status(self, user_id: int, status: str) -> list[Movie]:
        """Get all movies for a user with a specific status."""
        return Movie.query.join(UserMovieStatus).filter(
            UserMovieStatus.user_id == user_id,
            UserMovieStatus.status == status
        ).all()

    def get_user_watch_history(self, user_id: int) -> list[UserMovieStatus]:
        """Get the watch history for a user, ordered by watch date."""
        return UserMovieStatus.query.filter_by(user_id=user_id, status='watched').order_by(UserMovieStatus.watched_at.desc()).all()

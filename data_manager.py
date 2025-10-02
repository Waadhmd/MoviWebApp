from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Movie

class DataManager:
    """Handles CRUD operations for users and movies """
    # User Operation
    def create_user(self,name:str) -> User:
        """Create and add a new user to the database"""
        try:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user : {e}")
            return None

    def get_users(self):
        """Return all users from the database"""
        try:
            return User.query.all()
        except SQLAlchemyError as e :
            print(f"Error fetching users : {e}")
            return []

    #Movie Operation
    def get_movies(self,user_id:int) -> list[Movie]:
        """Return all movies belonging to a specific user"""
        try:
            return Movie.query.filter(user_id = user_id).all()
        except SQLAlchemyError as e :
            print(f"Error fetching movies for user {user_id} : {e}")
            return []

    def add_movie(self,movie:Movie) -> Movie:
        """Add Movie to the database.
         ensures that the user exists before adding"""
        try:
            user = User.query.get(movie.user_id)
            if not user:
                print(f"Cannot add movie : user_id {movie.user_id} doesn't exist")
                return None

            db.session.add(movie)
            db.session.commit()
            return movie

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding Movie :{e}")
            return None

    def update_movie(self, movie_id: int, user_id: int, new_title: str) -> Movie | None:
        """Update the title of a movie only if it belongs to the given user."""
        try:
            movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
            if movie:
                movie.name = new_title
                db.session.commit()
                return movie
            else:
                print(f"Movie with id {movie_id} not found for user {user_id}.")
                return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating movie: {e}")
            return None



    def delete_movie(self, movie_id:int, user_id:int) -> bool:
        """Delete a movie only if it belongs to the given user"""
        try:
            movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
            if movie:
                db.session.delete()
                db.session.commit()
                return  True
            else:
                print(f"Movie with id {movie_id} not found.")
                return False
        except SQLAlchemyError as e :
            print(f"Error deleting movie {e}")
            return False










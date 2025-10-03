
from flask import Flask, render_template, request, url_for, redirect
from data_manager import DataManager
from models import db, Movie, User
import os
from services.omdb_api import fetch_movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app.
data_manager = DataManager() # Create an object of your DataManager class


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name', '').strip()
    if name:
        data_manager.create_user(name)
    return redirect(url_for('index'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """Show user's favorite movies"""
    user = User.query.get(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    try:
        title = request.form.get('name', '').strip()
        if not title:
            return redirect(url_for('get_movies', user_id=user_id))

        movie = fetch_movie(title, user_id)
        if movie:
            data_manager.add_movie(movie)

        return redirect(url_for('get_movies', user_id=user_id))
    except Exception as e:
        print(f"Unexpected error in add_movie route: {e}")
        return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update movie title"""
    new_title = request.form.get('new_title', '').strip()
    if new_title:
        data_manager.update_movie(movie_id, user_id, new_title)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie"""
    data_manager.delete_movie(movie_id, user_id)
    return redirect(url_for('get_movies', user_id=user_id))

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
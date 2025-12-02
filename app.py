import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from data_manager import DataManager
from models import db, Movie, User
from services.omdb_api import fetch_movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'a-very-secret-key')

db.init_app(app)
data_manager = DataManager()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
     user = data_manager.find_user_by_id(int(user_id))
     print("Loaded user:", user, "Type:", type(user))
     return user

@app.cli.command('init-db')
def init_db():
    """Create all database tables."""
    with app.app_context():
        db.create_all()
    print("Database initialized.")

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movies'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = data_manager.find_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('movies'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if data_manager.find_user_by_username(username):
            flash('Username already exists')
        else:
            user = data_manager.create_user(username, email, password)
            if user:
                flash('Registration successful! Please log in.')
                return redirect(url_for('login'))
            else:
                flash('An error occurred during registration.')

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- Movie and Profile Routes ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('movies'))
    return redirect(url_for('login'))

@app.route('/movies')
@login_required
def movies():
    user_movies_with_status = data_manager.get_user_movies_with_status(current_user.id)
    return render_template('movies.html', movies_with_status=user_movies_with_status, user=current_user)

@app.route('/add_movie', methods=['POST'])
@login_required
def add_movie():
    title = request.form.get('name', '').strip()
    if title:
        movie_data = fetch_movie(title)
        if movie_data:
            rating_str = movie_data.get('imdbRating')
            rating = float(rating_str) if rating_str and rating_str != 'N/A' else None
            data_manager.add_movie(
                name=movie_data['Title'],
                director=movie_data['Director'],
                year=int(movie_data['Year']),
                poster_url=movie_data['Poster'],
                rating=rating,
                user_id=current_user.id
            )
        else:
            flash('Movie not found in OMDb.')
    return redirect(url_for('movies'))


@app.route('/movie/<int:movie_id>/status', methods=['POST'])
@login_required
def set_movie_status(movie_id):
    status = request.form.get('status')
    if status in ['watched', 'want-to-watch']:
        data_manager.set_user_movie_status(current_user.id, movie_id, status)
        return jsonify({'success': True, 'status': status})
    return jsonify({'success': False, 'error': 'Invalid status'}), 400

@app.route('/profile')
@login_required
def profile():
    watch_history = data_manager.get_user_watch_history(current_user.id)
    total_watched = len(watch_history)

    # Streak calculation
    daily_streak = 0
    weekly_streak = 0
    if watch_history:
        today = datetime.utcnow().date()
        # Daily streak
        last_watched_date = watch_history[0].watched_at.date()
        if last_watched_date == today or last_watched_date == today - timedelta(days=1):
            daily_streak = 1
            for i in range(1, len(watch_history)):
                current_date = watch_history[i-1].watched_at.date()
                previous_date = watch_history[i].watched_at.date()
                if current_date - previous_date == timedelta(days=1):
                    daily_streak += 1
                else:
                    break
        
        # Weekly streak
        start_of_this_week = today - timedelta(days=today.weekday())
        watched_weeks = {w.watched_at.date().isocalendar()[1] for w in watch_history}
        if start_of_this_week.isocalendar()[1] in watched_weeks:
            weekly_streak = 1
            current_week = start_of_this_week.isocalendar()[1]
            while (current_week - 1) in watched_weeks:
                weekly_streak += 1
                current_week -= 1


    return render_template('profile.html', user=current_user, total_watched=total_watched, daily_streak=daily_streak, weekly_streak=weekly_streak)


@app.route('/dashboard')
#@login_required
def dashboard():
    sort_by = request.args.get('sort_by')
    all_movies = data_manager.get_all_movies()
    if sort_by == 'rating':
        all_movies.sort(key=lambda x: x.rating if x.rating is not None else -1, reverse=True)
    elif sort_by == 'year':
        all_movies.sort(key=lambda x: x.year, reverse=True)
    return render_template('dashboard.html', movies=all_movies)


# --- Error Handler ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
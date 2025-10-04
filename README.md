## 🎬 CineShelf App

CineShelf is a simple Flask web application that allows cinephiles to:
- Create users (cinephiles).
- Add favorite movies to each user’s library (fetched from the [OMDb API](http://www.omdbapi.com/)).
- View, update, and delete movies from a user’s collection.
## Live Demo
Check out the live version of this project: [CineShelf](https://waad94.eu.pythonanywhere.com/)

## 🚀 Features
- User management (create, list).
- Movie management (add, update, delete).
- OMDb API integration to fetch movie details.
- Styled with [Bootstrap](https://getbootstrap.com/) and custom CSS.
- SQLite database with SQLAlchemy ORM.

## Install dependencies
pip install -r requirements.txt

## Set up environment variables
Create a .env file (or export directly in your shell):
export API_KEY=your_omdb_api_key

## Initialize the database
>>> from models import db
>>> from app import app
>>> with app.app_context():
...     db.create_all()
> 
## Run the app
flask run
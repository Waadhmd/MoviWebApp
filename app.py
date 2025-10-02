from crypt import methods

from flask import Flask
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app.

data_manager = DataManager() # Create an object of your DataManager class

# Create tables (if not exist)
# -------------------------
#with app.app_context():
 #   user = data_manager.create_user('waad')

@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


if __name__ == '__main__':
    app.run(debug=True)
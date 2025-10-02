from models import Movie
import requests
import os
from requests.exceptions import RequestException

OMDB_URL = "http://www.omdbapi.com/"
API_KEY = os.getenv("API_KEY")

def fetch_movie(title: str, user_id: int) -> Movie | None:
    """Fetch movie data from OMDb and return a Movie object ready for DB insertion."""
    params = {"t": title, "apikey": API_KEY}
    try:
        response = requests.get(OMDB_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            movie = Movie(
                name=data.get("Title"),
                director=data.get("Director"),
                year=int(data.get("Year", 0)),
                poster_url=data.get("Poster"),
                user_id=user_id
            )
            return movie
        else:
            print(f"OMDb Error: {data.get('Error')}")
            return None

    except RequestException as e:
        print(f"HTTP Error: {e}")
        return None



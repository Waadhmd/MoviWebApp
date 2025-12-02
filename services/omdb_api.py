import requests
import os
from requests.exceptions import RequestException

OMDB_URL = "http://www.omdbapi.com/"
API_KEY = os.environ.get("API_KEY")

def fetch_movie(title: str) -> dict | None:
    """Fetch movie data from OMDb and return a dictionary."""
    params = {"t": title, "apikey": API_KEY}
    try:
        response = requests.get(OMDB_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            return data
        else:
            print(f"OMDb Error: {data.get('Error')}")
            return None

    except RequestException as e:
        print(f"HTTP Error: {e}")
        return None

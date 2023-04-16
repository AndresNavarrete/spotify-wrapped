import base64
import os
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv


class Spotify:
    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.REDIRECT_URI = os.getenv("REDIRECT_URI")
        self.ACTIVATION_CODE = os.getenv("ACTIVATION_CODE")
        self.REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
        self.access_token = None
        self.top_tracks = None

    def refresh_access_token(self):
        auth_header = base64.b64encode(
            f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode("utf-8")
        ).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"grant_type": "refresh_token", "refresh_token": self.REFRESH_TOKEN}
        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )
        tokens = response.json()
        self.access_token = tokens["access_token"]

    def get_top_tracks(self):
        self.refresh_access_token()
        self.fetch_top_tracks()
        return self.top_tracks

    def fetch_top_tracks(self):
        base_url = "https://api.spotify.com/v1/me/top/tracks"
        query_params = {
            "time_range": "medium_term",
            "limit": 50,
        }
        url = base_url + "?" + urlencode(query_params)

        headersList = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.request("GET", url, headers=headersList)
        self.top_tracks = response.json()["items"]

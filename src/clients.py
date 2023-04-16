import base64
import os
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

#
# Documentation
# Endpoint -  https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
# Auth     -  https://developer.spotify.com/documentation/web-api/tutorials/code-flow
#


class Spotify:
    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.REDIRECT_URI = os.getenv("REDIRECT_URI")
        self.ACTIVATION_CODE = os.getenv("ACTIVATION_CODE")
        self.REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

        self.items_time_range = "short_term"
        self.items_limit = 50

        self.access_token = None
        self.top_tracks = None
        self.top_artists = None

    def get_top_tracks(self):
        self.refresh_access_token()
        self.fetch_top_tracks()
        return self.top_tracks

    def get_top_artists(self):
        self.refresh_access_token()
        self.fetch_top_artists()
        return self.top_artists

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

    def get_top_items(self, base_url):
        query_params = {
            "time_range": self.items_time_range,
            "limit": self.items_limit,
        }
        url = base_url + "?" + urlencode(query_params)

        headersList = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.request("GET", url, headers=headersList)
        return response.json()["items"]

    def fetch_top_tracks(self):
        base_url = "https://api.spotify.com/v1/me/top/tracks"
        self.top_tracks = self.get_top_items(base_url)

    def fetch_top_artists(self):
        base_url = "https://api.spotify.com/v1/me/top/artists"
        self.top_artists = self.get_top_items(base_url)

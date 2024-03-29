import base64
import os
from urllib.parse import urlencode

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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


class Postgres:
    def __init__(self):
        load_dotenv()
        self.PG_HOST = os.getenv("POSTGRES_HOST")
        self.PG_PORT = os.getenv("POSTGRES_PORT")
        self.PG_DB = os.getenv("POSTGRES_DB")
        self.PG_USER = os.getenv("POSTGRES_USER")
        self.PG_PASS = os.getenv("POSTGRES_PASSWORD")
        self.engine = None
        self.conn = None
        self.set_engine()

    def set_engine(self):
        uri_str = f"postgresql+psycopg2://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        self.engine = create_engine(uri_str)

    def write_workspace(self, data, table_name):
        with self.engine.connect() as connection:
            data.to_sql(
                f"workspace_{table_name}",
                con=connection,
                schema="public",
                if_exists="append",
                index=False,
            )

    def execute_raw_query(self, query):
        with self.engine.connect() as connection:
            trans = connection.begin()
            connection.execute(text(query))
            trans.commit()

    def fetch_query(self, query):
        return pd.read_sql(sql=query, con=self.engine)


class ExternalAPI:
    def __init__(self):
        self.hostname = os.getenv("API_URL")
        self.user = os.getenv("DJANGO_ANON_USER")
        self.password = os.getenv("DJANGO_ANON_PASSWORD")
        self.artists_endpoint = f"{self.hostname}/artists_ranking_details"
        self.tracks_endpoint = f"{self.hostname}/tracks_ranking_details"

    def fetch_artists_ranking(self):
        response = self.fetch_response(self.artists_endpoint, auth=self.get_auth())
        return self.get_dataframe_from_response(response)

    def fetch_tracks_ranking(self):
        response = self.fetch_response(self.tracks_endpoint, auth=self.get_auth())
        return self.get_dataframe_from_response(response)

    def fetch_response(self, url, auth):
        response = requests.get(url, auth=auth)
        if response.status_code != 200:
            raise ValueError(f"Status code in response: {response.status_code}")
        return response.json()

    def get_auth(self):
        return (self.user, self.password)

    def get_dataframe_from_response(self, response):
        return pd.DataFrame().from_records(response)

    def download_artist_ranking(self, path_to_download):
        self.check_directory_existence(path_to_download)
        artists = self.fetch_artists_ranking()
        json_data = artists.to_json(orient="records", indent=6)
        with open(path_to_download, "w", encoding="utf-8") as file:
            file.write(json_data)

    def download_tracks_ranking(self, path_to_download):
        self.check_directory_existence(path_to_download)
        tracks = self.fetch_tracks_ranking()
        json_data = tracks.to_json(orient="records", indent=6)
        with open(path_to_download, "w", encoding="utf-8") as file:
            file.write(json_data)

    def check_directory_existence(self, path_to_download):
        directory = os.path.dirname(path_to_download)
        if not os.path.exists(directory):
            os.makedirs(directory)

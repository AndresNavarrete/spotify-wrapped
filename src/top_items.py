from src.clients import Postgres, Spotify
from src.datasets import ArtistDataset, TracksDataset
from src.models import Artist, Track


def get_top_tracks():
    postgres = Postgres()
    spotify = Spotify()

    tracks = [Track(item) for item in spotify.get_top_tracks()]

    tracks_dataset = TracksDataset(tracks)
    dataframe = tracks_dataset.get_dataset()
    postgres.write_workspace(data=dataframe, table_name="tracks")


def get_top_artists():
    postgres = Postgres()
    spotify = Spotify()

    artists = [Artist(item) for item in spotify.get_top_tracks()]

    tracks_dataset = ArtistDataset(artists)
    dataframe = tracks_dataset.get_dataset()
    postgres.write_workspace(data=dataframe, table_name="artists")

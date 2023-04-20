import sys

from src.clients import Postgres, Spotify
from src.datasets import ArtistDataset, TracksDataset
from src.models import Artist, Track


def main():
    item = sys.argv[1]
    if item == "artists":
        get_top_artists()
    elif item == "tracks":
        get_top_tracks()
    else:
        raise SystemExit("Error: incorrect item")


def get_top_tracks():
    postgres = Postgres()
    spotify = Spotify()

    tracks = [Track(item) for item in spotify.get_top_tracks()]

    dataset = TracksDataset(tracks)
    dataframe = dataset.get_dataset()
    postgres.write_workspace(data=dataframe, table_name="tracks")


def get_top_artists():
    postgres = Postgres()
    spotify = Spotify()

    artists = [Artist(item) for item in spotify.get_top_artists()]

    dataset = ArtistDataset(artists)
    dataframe = dataset.get_dataset()
    postgres.write_workspace(data=dataframe, table_name="artists")


if __name__ == "__main__":
    main()

from src.clients import Postgres, Spotify
from src.datasets import ArtistDataset, TracksDataset
from src.models import Artist, Track

postgres = Postgres()
spotify = Spotify()

tracks = list()
artists = list()

items = spotify.get_top_tracks()
for item in items:
    tracks.append(Track(item))

tracks_dataset = TracksDataset(tracks)
dataframe = tracks_dataset.get_dataset()
postgres.write_workspace(data=dataframe, table_name="tracks")


items = spotify.get_top_artists()
for item in items:
    artists.append(Artist(item))

artist_dataset = ArtistDataset(artists)
dataframe = artist_dataset.get_dataset()
postgres.write_workspace(data=dataframe, table_name="artists")

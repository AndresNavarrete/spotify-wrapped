from src.clients import Spotify
from src.models import Artist, Track

spotify = Spotify()
tracks = list()

items = spotify.get_top_tracks()
for item in items:
    track = Track(item)
    print(track)

print("\n\n")

items = spotify.get_top_artists()
for item in items:
    artist = Artist(item)
    print(artist)

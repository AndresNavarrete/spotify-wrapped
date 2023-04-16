from src.clients import Spotify
from src.models import Track

spotify = Spotify()
tracks = list()

items = spotify.get_top_tracks()
for item in items:
    track = Track(item)
    print(track)

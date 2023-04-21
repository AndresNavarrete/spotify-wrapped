from dataclasses import dataclass


@dataclass
class Track:
    def __init__(self, item):
        self.id = item["id"]
        self.artist_id = item["artists"][0]["id"]
        self.album_id = item["album"]["id"]
        self.name = item["name"]
        self.artist = item["artists"][0]["name"]
        self.spotify_url = item["external_urls"]["spotify"]
        self.album_image_url = item["album"]["images"][0]["url"]

    def __str__(self) -> str:
        return f"{self.artist:30} | {self.name:30}"


@dataclass
class Artist:
    def __init__(self, item):
        self.id = item["id"]
        self.name = item["name"]
        self.spotify_url = item["external_urls"]["spotify"]
        try:
            self.image_url = item["images"][0]["url"]
        except Exception as e:
            print(f"Error: {e} on {self.name}")
            self.image_url = None

    def __str__(self) -> str:
        return f"{self.name}"

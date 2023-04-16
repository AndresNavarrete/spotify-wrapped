class Track:
    def __init__(self, item):
        self.id = item["id"]
        self.atrist_id = item["artists"][0]["id"]
        self.album_id = item["album"]["id"]
        self.name = item["name"]
        self.artist = item["artists"][0]["name"]
        self.spotify_url = item["external_urls"]["spotify"]
        self.album_image_url = item["album"]["images"][0]["url"]

    def __str__(self) -> str:
        return f"{self.artist:30} | {self.name:30}"

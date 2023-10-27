from src.clients import ExternalAPI

if __name__ == "__main__":
    api = ExternalAPI()
    api.download_artist_ranking("data/artists.json")
    api.download_tracks_ranking("data/tracks.json")

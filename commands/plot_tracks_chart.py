from src.content_generator import ContentGenerator
from src.queries_manager import Queries_Manager

if __name__ == "__main__":
    items_name = "track"
    item_url_name = "album_image_url"
    query = Queries_Manager().get_sql_script("plot_tracks_chart")
    ContentGenerator(query, items_name, item_url_name).make_chart()

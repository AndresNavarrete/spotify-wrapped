from src.content_generator import ContentGenerator
from src.queries_manager import Queries_Manager

if __name__ == "__main__":
    items_name = "artist"
    item_url_name = "artist_image_url"
    query = Queries_Manager().get_sql_script("plot_artists_chart")
    ContentGenerator(query, items_name, item_url_name).make_chart()

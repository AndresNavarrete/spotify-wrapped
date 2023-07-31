from src.queries_manager import Queries_Manager
from src.ranking_plotter import RankingImageGenerator

if __name__ == "__main__":
    query = Queries_Manager().get_sql_script("plot_tracks_days_in_top")
    RankingImageGenerator(query, title="Top songs - days in top 3").save_ranking_image(
        "ranking_songs.png"
    )
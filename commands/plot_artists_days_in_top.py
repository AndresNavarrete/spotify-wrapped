from src.ranking_plotter import RankingImageGenerator

if __name__ == "__main__":
    RankingImageGenerator(
        items="artists", title="All time Top artists - Days in top 3"
    ).save_ranking_image("ranking_artists.png")

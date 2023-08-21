from src.ranking_plotter import RankingImageGenerator

if __name__ == "__main__":
    RankingImageGenerator(
        items="tracks", title="All time Top songs - Days in top 3"
    ).save_ranking_image("ranking_songs.png")

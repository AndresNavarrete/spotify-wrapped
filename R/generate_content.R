source('R/utils.R')
source('R/data_processing.R')

# Load required libraries
load_libraries()

# Load data
artists <- load_data("data/artists.json")
tracks <- load_data("data/tracks.json")

# Data manipulation
artists$image_url <- circle_crop(artists$image_url)
tracks$image_url <- circle_crop(tracks$image_url)

# Process data and create plots
df_artists <- process_data(artists, artists)
plot_artists <- create_plot(df_artists, "All time Top artists - Days in top 3")
save_plot(plot_artists, "img/ranking_artists.png")

df_tracks <- process_data(tracks, tracks)
plot_tracks <- create_plot(df_tracks, "All time Top songs - Days in top 3")
save_plot(plot_tracks, "img/ranking_songs.png")

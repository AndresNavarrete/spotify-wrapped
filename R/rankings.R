
# Load required libraries  ----------------------------------------------------------------------
if (!require(ggplot2)) {
  install.packages('ggplot2')
}
if (!require(jsonlite)) {
  install.packages('jsonlite')
}
if (!require(ggimage)) {
  install.packages('ggimage')
}
if (!require(devtools)) {
  install.packages('devtools')
}
if (!require(cropcircles)) {
  install.packages('cropcircles')
}
if (!require(dplyr)) {
  install.packages('dplyr')
}
if (!require(tidyr)) {
  install.packages('tidyr')
}

library(ggplot2)
library(jsonlite)
library(ggimage)
library(cropcircles)
library(dplyr)
library(tidyr)


# Load data ----------------------------------------------------------------------
artists <- fromJSON("data/artists.json")
df_artists <- as.data.frame(artists)

tracks <- fromJSON("data/tracks.json")
df_tracks <- as.data.frame(tracks)

# Data manipulation ----------------------------------------------------------------------
df_artists$image_url <- circle_crop(df_artists$image_url)
df_tracks$image_url <- circle_crop(df_tracks$image_url)


names <- c ("Last week", "Last month", "Last 2 months", "Before")

BACKGROUND_COLOR <- "#D9D9D9"


# Date on top Plot - Tracks----------------------------------------------------------------------


new_df <- df_tracks %>%
  arrange(desc(count_total)) %>%
  slice_head(n = 15) %>%
  pivot_longer(cols = c(count_last_7, count_last_30, count_last_60, count_prev), 
               names_to = "count_type", 
               values_to = "value")%>%
  left_join(df_tracks %>% select(name, image_url), by = "name")%>%
  rename(image_url = image_url.x)%>%
  mutate(count_type = case_when(
    count_type == "count_last_7" ~ "Last week",
    count_type == "count_last_60" ~ "Last 2 months",
    count_type == "count_last_30" ~ "Last month",
    count_type == "count_prev" ~ "Before"
  ))

new_df$name <- reorder(new_df$name, ave(new_df$value, new_df$name, FUN = sum))

p <- ggplot(data = new_df, aes(x = value, y = reorder(name, ave(value, name, FUN = sum)), fill = count_type)) +
  geom_bar(stat = "identity") +
  geom_image(aes(image = image_url), x = -0.5, size = 0.06) +
  labs(x = "Days", y = "", title = "All time Top songs - Days in top 3", fill = "Date in top") +
  theme_minimal() +
  theme(
    plot.background = element_rect(fill = BACKGROUND_COLOR),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    legend.position = c(.95, .05),  
    legend.justification = c("right", "bottom"),
    legend.background = element_rect(fill = "transparent") ,
    legend.text = element_text(size = 12) ,
    axis.text.y = element_text(size = 13) ,
    plot.title = element_text(size = 20, face = "bold") 
  )

ggsave(filename = "img/ranking_songs.png", plot = p, dpi = 600, width = 12, height = 8)


# Date on top Plot - Tracks----------------------------------------------------------------------


new_df <- df_artists %>%
  arrange(desc(count_total)) %>%
  slice_head(n = 15) %>%
  pivot_longer(cols = c(count_last_7, count_last_30, count_last_60, count_prev), 
               names_to = "count_type", 
               values_to = "value")%>%
  left_join(df_artists %>% select(name, image_url), by = "name")%>%
  rename(image_url = image_url.x)%>%
  mutate(count_type = case_when(
    count_type == "count_last_7" ~ "Last week",
    count_type == "count_last_60" ~ "Last 2 months",
    count_type == "count_last_30" ~ "Last month",
    count_type == "count_prev" ~ "Before"
  ))

new_df$name <- reorder(new_df$name, ave(new_df$value, new_df$name, FUN = sum))

p <- ggplot(data = new_df, aes(x = value, y = reorder(name, ave(value, name, FUN = sum)), fill = count_type)) +
  geom_bar(stat = "identity") +
  geom_image(aes(image = image_url), x = -0.5, size = 0.06) +
  labs(x = "Days", y = "", title = "All time Top Artists - Days in top 3", fill = "Date in top") +
  theme_minimal() +
  theme(
    plot.background = element_rect(fill = BACKGROUND_COLOR),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    legend.position = c(.95, .05),  
    legend.justification = c("right", "bottom"),
    legend.background = element_rect(fill = "transparent") ,
    legend.text = element_text(size = 12) ,
    axis.text.y = element_text(size = 13) ,
    plot.title = element_text(size = 20, face = "bold") 
  )

ggsave(filename = "img/ranking_artists.png", plot = p, dpi = 600,  width = 12, height = 8)

process_data <- function(df, df_join) {
  df %>%
    arrange(desc(count_total)) %>%
    slice_head(n = 15) %>%
    pivot_longer(cols = c(count_last_7, count_last_30, count_last_60, count_prev), 
                 names_to = "count_type", 
                 values_to = "value") %>%
    left_join(df_join %>% select(name, image_url), by = "name") %>%
    rename(image_url = image_url.x) %>%
    mutate(count_type = case_when(
      count_type == "count_last_7" ~ "Last week",
      count_type == "count_last_60" ~ "Last 2 months",
      count_type == "count_last_30" ~ "Last month",
      count_type == "count_prev" ~ "Before"
    )) %>%
    mutate(name = reorder(name, ave(value, name, FUN = sum)))
}

create_plot <- function(df, title) {
  BACKGROUND_COLOR <- "#D9D9D9"
  ggplot(data = df, aes(x = value, y = name, fill = count_type)) +
    geom_bar(stat = "identity") +
    geom_image(aes(image = image_url), x = -0.5, size = 0.06) +
    labs(x = "Days", y = "", title = title, fill = "Date in top") +
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
}

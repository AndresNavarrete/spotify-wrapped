load_libraries <- function() {
  libraries <- c('ggplot2', 'jsonlite', 'ggimage', 'cropcircles', 'dplyr', 'tidyr')
  for (lib in libraries) {
    if (!require(lib, character.only = TRUE)) {
      install.packages(lib)
    }
  }
}

load_data <- function(file_path) {
  fromJSON(file_path) %>% as.data.frame()
}

save_plot <- function(plot, filename) {
  ggsave(filename = filename, plot = plot, dpi = 600, width = 12, height = 8)
}

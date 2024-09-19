# Load required libraries
library(ggvenn)
library(ggplot2)
library(readr)

# Function to read CSV files from a directory
read_csv_files <- function(directory) {
  csv_files <- list.files(path = directory, pattern = "*.csv", full.names = TRUE)
  data_list <- list()
  
  for (file in csv_files) {
    set_name <- tools::file_path_sans_ext(basename(file))
    data <- read_csv(file, col_names = FALSE)
    data_list[[set_name]] <- data[[1]]
  }
  
  return(data_list)
}

# Read CSV files from the specified directory
data <- read_csv_files("Results/02_DF_Distribution/02_Venn/Defense_Type/Location")

# Create a color palette for the sets
num_sets <- length(data)

# Fix: Replace the invalid "#" with a valid color code
color_palette <- colorRampPalette(c("#FF0000FF", "#EFC000FF", "#868686FF", "#CD534CFF"))(num_sets)

# Create Venn diagram
venn_plot <- ggvenn(
  data,
  fill_color = color_palette,
  stroke_size = 0.5,
  set_name_size = 4
)

# Customize the plot
venn_plot <- venn_plot +
  theme_void() +
  ggtitle("Venn Diagram of CSV Data") +
  theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"))

# Display the plot
print(venn_plot)

# Save the plot as a PNG file
ggsave("venn_diagram.png", venn_plot, width = 10, height = 8, dpi = 300)

# Print a message
cat("Venn diagram has been created and saved as 'venn_diagram.png'")

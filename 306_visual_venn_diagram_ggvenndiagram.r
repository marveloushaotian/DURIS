# Load required libraries
library(ggVennDiagram)
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
data <- read_csv_files("Results/02_DF_Distribution/02_Venn/Defense_Subtype/Country")

# Create Venn diagram
venn_plot <- ggVennDiagram(
  label_alpha = 0,
  label_percent_digit = 1,
  label_size = 8,
  data,
  category.names = names(data),
  label = "percent",
  edge_size = 0.5,
  set_size = 8
) +
  scale_fill_gradient(low = "#e8e7e9", high = "#a673a3") + 
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
        legend.position = "none")

# Display the plot
print(venn_plot)

# Save the plot as a PNG file
ggsave("Results/02_DF_Distribution/02_Venn/venn_subtype_country.png", venn_plot, width = 10, height = 8, dpi = 300)

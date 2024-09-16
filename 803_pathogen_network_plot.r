# Load required libraries
library(tidyverse)
library(igraph)
library(ggraph)

# Function to draw network graph
draw_network_graph <- function(input_file, output_pdf, output_png) {
  # 1. Read the input CSV file
  df <- read_csv(input_file)
  
  # 2. Create an empty graph
  g <- graph.empty(directed = FALSE)
  
  # 3. Add nodes and edges
  for (i in 1:nrow(df)) {
    kaiju_species <- df$Kaiju_Species[i]
    defense_type <- df$Defense_Type[i]
    count <- df$Count[i]
    gcgb <- df$GCGB[i]
    
    # Add nodes
    if (!(kaiju_species %in% V(g)$name)) {
      g <- add_vertices(g, 1, name = kaiju_species, size = 0, color = "skyblue")
    }
    if (!(defense_type %in% V(g)$name)) {
      g <- add_vertices(g, 1, name = defense_type, size = 0, color = "lightgreen")
    }
    
    # Add edges and accumulate node size information
    g <- add_edges(g, c(kaiju_species, defense_type), weight = gcgb)
    V(g)[defense_type]$size <- V(g)[defense_type]$size + gcgb
  }
  
  # 4. Update Kaiju_Species node sizes based on the sum of GCGB of connected Defense_Type nodes
  for (v in V(g)[color == "skyblue"]) {
    connected_defense_types <- neighbors(g, v)
    V(g)[v]$size <- sum(V(g)[connected_defense_types]$size)
  }
  
  # 5. Scale node sizes
  V(g)$size <- V(g)$size * 0.1
  
  # 6. Create the plot
  p <- ggraph(g, layout = "fr") +
    geom_edge_link(aes(width = weight), alpha = 0.5, color = "gray") +
    geom_node_point(aes(size = size, color = color)) +
    geom_node_text(aes(label = name), repel = TRUE, size = 3) +
    scale_edge_width(range = c(0.1, 2)) +
    scale_size(range = c(1, 10)) +
    scale_color_identity() +
    theme_void() +
    theme(legend.position = "none")
  
  # 7. Save the output images as PDF and PNG
  ggsave(output_pdf, p, width = 24, height = 16, units = "in", dpi = 300)
  ggsave(output_png, p, width = 24, height = 16, units = "in", dpi = 300)
}

# Function to process directory
process_directory <- function(input_dir, output_dir) {
  # Ensure the output directory exists
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  
  # Get a list of all CSV files in the input directory
  csv_files <- list.files(input_dir, pattern = "\\.csv$", full.names = TRUE)
  
  # Process each file
  for (input_file in csv_files) {
    output_pdf <- file.path(output_dir, gsub("\\.csv$", ".pdf", basename(input_file)))
    output_png <- file.path(output_dir, gsub("\\.csv$", ".png", basename(input_file)))
    draw_network_graph(input_file, output_pdf, output_png)
    cat("Processed files saved:", output_pdf, "and", output_png, "\n")
  }
}

# Main execution
main <- function() {
  # Set input and output paths here
  input_path <- "Results/Network/All_defense_info_sing_splited_pathogen"
  output_path <- "Results/Network/All_defense_info_sing_splited_table_plot"
  
  if (dir.exists(input_path)) {
    process_directory(input_path, output_path)
  } else {
    output_pdf <- file.path(output_path, "network_graph.pdf")
    output_png <- file.path(output_path, "network_graph.png")
    draw_network_graph(input_path, output_pdf, output_png)
  }
}

# Run the main function
main()
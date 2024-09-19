library(tidyverse)

# Read the data
df <- read_csv("Collect/All_contigs_info_muti_defense.csv")


process_data <- function(df, filter_defense = FALSE) {
  # Filter out empty or 'No' values in Kaiju_Phylum
  df <- df %>% 
    filter(!is.na(Kaiju_Phylum) & Kaiju_Phylum != 'No')
  
  if (filter_defense) {
    df <- df %>% 
      filter(!is.na(Defense_Type) & Defense_Type != 'No')
  }
  
  # Group by Country, Location, and Kaiju_Phylum
  grouped <- df %>%
    group_by(Country, Location, Kaiju_Phylum) %>%
    summarise(count = n(), .groups = 'drop') %>%
    pivot_wider(names_from = Kaiju_Phylum, values_from = count, values_fill = 0)
  
  # Calculate percentages
  percentages <- grouped %>%
    mutate(across(-c(Country, Location), ~ . / sum(.) * 100))
  
  # Sort columns by total percentage (descending) and keep top 20
  top_20 <- percentages %>%
    select(-Country, -Location) %>%
    colSums() %>%
    sort(decreasing = TRUE) %>%
    head(20) %>%
    names()
  
  # Combine remaining phyla into 'Others'
  percentages <- percentages %>%
    mutate(Others = rowSums(select(., -c(Country, Location, all_of(top_20))))) %>%
    select(Country, Location, all_of(top_20), Others)
  
  # Sort columns by total abundance (ascending)
  col_order <- percentages %>%
    select(-Country, Location) %>%
    colSums() %>%
    sort() %>%
    names()
  
  percentages %>%
    select(Country, Location, all_of(col_order))
}

plot_stacked_bar <- function(data, title, output_file) {
  colors <- c("#c0dbe6","#2b526f","#4a9ba7","#a3cbd6","#c0cfbd","#9bb88a","#7b9b64","#d0cab7","#c6a4c5","#9b7baa","#7a7aaf","#434d91","#5284a2","#82b4c8","#9d795d","#d1b49a","#fff08c","#e1834e","#cd6073","#ffc7c9","#969696","#d1d9e2")
  
  # Prepare data for plotting
  plot_data <- data %>%
    pivot_longer(cols = -c(Country, Location), names_to = "Phylum", values_to = "Percentage")
  
  # Create the plot
  p <- ggplot(plot_data, aes(x = Location, y = Percentage, fill = Phylum)) +
    geom_bar(stat = "identity", position = "stack", width = 0.7) +
    facet_wrap(~ Country, scales = "free_x", nrow = 1) +
    scale_fill_manual(values = colors) +
    labs(title = title,
         y = "Abundance of Taxonomy",
         x = "") +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 20, face = "bold"),
      axis.title.y = element_text(size = 14, face = "bold"),
      axis.text = element_text(size = 12),
      axis.text.x = element_text(angle = 0, hjust = 0.5, face = "bold"),
      legend.position = "right",
      legend.title = element_blank(),
      strip.text = element_text(size = 16, face = "bold")
    )
  
  # Save the plot
  ggsave(output_file, p, width = 20, height = 8, dpi = 300)
  cat(sprintf("Chart saved as %s\n", output_file))
}

# Process data for both charts
data_all <- process_data(df)
data_defense <- process_data(df, filter_defense = TRUE)

# Ensure consistent legend for both charts
all_phyla <- union(names(data_all), names(data_defense))
data_all[setdiff(all_phyla, names(data_all))] <- 0
data_defense[setdiff(all_phyla, names(data_defense))] <- 0

# Create the plots
plot_stacked_bar(data_all, 'All Contigs', "all_contigs.png")
plot_stacked_bar(data_defense, 'Contigs with Defense Systems', "defense_contigs.png")

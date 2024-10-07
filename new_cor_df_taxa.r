# Load required libraries
library(tidyverse)
library(ggplot2)
library(gridExtra)

# Read the input files
phylum_data <- read.csv("Collect/all_samples_metaphlan_taxa_name_phylum.csv", row.names = 1)
defense_data <- read.csv("Collect/contigs_ab_df_sing_with_defense_grouped.csv", row.names = 1)
metadata <- read.csv("Collect/00_Metadata/Sample_Group.csv")  # Replace with the actual path to your metadata file

# Ensure both tables have the same sample columns
common_samples <- intersect(colnames(phylum_data), colnames(defense_data))
phylum_data <- phylum_data[, common_samples]
defense_data <- defense_data[, common_samples]

# Function to create a scatter plot with linear regression
create_correlation_plot <- function(phylum, defense, data, metadata) {
  cor_test <- cor.test(data$phylum_abundance, data$defense_abundance)
  cor_value <- round(cor_test$estimate, 3)
  p_value <- cor_test$p.value
  
  p_value_text <- if(p_value < 0.001) {
    "p < 0.001"
  } else {
    paste("p =", round(p_value, 3))
  }
  
  ggplot(data, aes(x = phylum_abundance, y = defense_abundance)) +
    geom_point(aes(color = Location, shape = Country)) +
    geom_smooth(method = "lm", se = TRUE, color = "red") +
    labs(title = paste(phylum, "vs", defense),
         x = paste(phylum, "Abundance"),
         y = paste(defense, "Abundance"),
         subtitle = paste("r =", cor_value, ",", p_value_text)) +
    theme_minimal() +
    theme(plot.title = element_text(size = 12),
          plot.subtitle = element_text(size = 10))
}

# Create output directory if it doesn't exist
dir.create("phylum_defense_correlations_sig", showWarnings = FALSE)

# Add a parameter to control whether to show only significant correlations
show_only_significant <- TRUE  # Set to TRUE to show only significant correlations

# Generate and save correlation plots grouped by defense
for (defense in rownames(defense_data)) {
  plots <- list()
  for (phylum in rownames(phylum_data)) {
    data <- data.frame(
      phylum_abundance = as.numeric(phylum_data[phylum, ]),
      defense_abundance = as.numeric(defense_data[defense, ]),
      sample = common_samples
    )
    
    # Merge with metadata
    data <- merge(data, metadata, by.x = "sample", by.y = "Sample")
    
    # Perform correlation test
    cor_test <- cor.test(data$phylum_abundance, data$defense_abundance)
    
    # Create plot if it meets the significance criteria or if showing all correlations
    if (!show_only_significant || (show_only_significant && cor_test$p.value < 0.01)) {
      plot <- create_correlation_plot(phylum, defense, data, metadata)
      plots[[phylum]] <- plot
    }
  }
  
  # Only save if there are plots to display
  if (length(plots) > 0) {
    # Arrange plots in a grid
    n_cols <- 3
    n_rows <- ceiling(length(plots) / n_cols)
    
    # Create a unique filename for each defense type
    filename <- paste0("phylum_defense_correlations_sig/", gsub(" ", "_", defense), "_correlations.pdf")
    
    # Save the plot grid as a PDF
    pdf(filename, width = 24, height = 8 * n_rows)
    do.call(grid.arrange, c(plots, ncol = n_cols))
    dev.off()
    
    cat("Saved plots for Defense Type:", defense, "as", filename, "\n")
  } else {
    cat("No plots created for Defense Type:", defense, "\n")
  }
}

cat("Correlation plots have been generated and saved in the 'phylum_defense_correlations_sig' directory.\n")
cat("To show only significant correlations, set 'show_only_significant' to TRUE.\n")

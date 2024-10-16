#!/usr/bin/env Rscript

# Load required libraries
library(vegan)
library(tidyverse)
library(ggplot2)

# 1. Load data
data <- read.csv("Collect/Defense_extracted.csv", row.names=1)
metadata <- read.csv("Collect/00_Metadata/Sample_Group.csv", row.names=1)

# 2. Calculate alpha diversity (Shannon index)
alpha_div <- diversity(t(data), index="shannon")
alpha_div_df <- data.frame(Sample = names(alpha_div), Alpha_Diversity = alpha_div)

# 3. Merge alpha diversity with metadata
merged_data <- merge(alpha_div_df, metadata, by.x="Sample", by.y="row.names")

# 4. Create boxplot for Country and Location interaction
plot_alpha_diversity <- function(data) {
  ggplot(data, aes(x = interaction(Country, Location), y = Alpha_Diversity, fill = Country)) +
    geom_boxplot() +
    geom_jitter(width = 0.2, alpha = 0.5) +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    labs(x = "Country and Location", y = "Alpha Diversity (Shannon)", 
         title = "Alpha Diversity by Country and Location") +
    scale_fill_brewer(palette = "Set3")
}

# Generate plot for Country and Location interaction
plot <- plot_alpha_diversity(merged_data)

# 5. Save results
# Save alpha diversity values
write.csv(alpha_div_df, file="alpha_diversity_results.csv", row.names=FALSE)

# Save plot
ggsave(filename="alpha_diversity_Country_Location.png", plot=plot, width=12, height=8, dpi=300)

cat("Analysis complete. Results saved.\n")

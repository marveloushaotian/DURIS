#!/usr/bin/env Rscript

# Load required libraries
library(tidyverse)
library(ggplot2)

# Set input and output file paths
input_file <- "Collect/All_contigs_info_muti_defense.csv"
output_file <- "correlation_plot.png"

# Read the input CSV file
if (!file.exists(input_file)) {
  stop("Input file does not exist: ", input_file)
}
data <- read.csv(input_file)

# Convert Defense_Number to numeric, replacing non-numeric values with NA
data$Defense_Number <- as.numeric(as.character(data$Defense_Number))

# Group by Country, Location, and Sample, then summarize
summary_data <- data %>%
  group_by(Country, Location, Sample) %>%
  summarize(
    Phage_Count = sum(Contig_Classification == "Phage"),
    Defense_Sum = sum(Defense_Number, na.rm = TRUE),
    .groups = 'drop'
  )

# Create scatter plot
ggplot(summary_data, aes(x = Phage_Count, y = Defense_Sum)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  facet_wrap(~ Country + Location, scales = "free") +
  theme_minimal() +
  labs(
    title = "Correlation between Phage Count and Defense Number Sum",
    x = "Phage Count",
    y = "Defense Number Sum"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5),
    strip.text = element_text(size = 8)
  )

# Save the plot
ggsave(output_file, width = 12, height = 8)

cat("Correlation plot has been saved to", output_file, "\n")

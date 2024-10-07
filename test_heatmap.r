# Load required libraries
library(tidyverse)
library(ComplexHeatmap)
library(circlize)

# Read the data
data <- read.csv("Collect/defense_type_summary_chromosome2.csv", row.names = 1)

# Transpose the data
data_transposed <- t(data)

# Log transform the transposed data
log_data <- log1p(data_transposed)

# Calculate column means for sorting
col_means <- colMeans(log_data)

# Sort the data by column means in descending order
sorted_data <- log_data[, order(col_means, decreasing = TRUE)]

# Save the log-transformed and sorted data
write.csv(sorted_data, "Collect/log_chromosome2.csv")

# Create a custom color map
create_custom_colormap <- function() {
  colors <- c("#8fced1", "#8ac2cd", "#86b7c8", "#81abc4", "#7ca0c0", "#7894bb", "#7389b7", "#6e7db3", "#6a72ae", "#6566aa", "#5b4fa1", "#513798", "#47208f")
  return(colorRamp2(c(0, 0.01, 0.05, 0.1, 0.5, 1, 2, 3, 4, 5, 6, 7 ,10), colors))
}

custom_cmap <- create_custom_colormap()

# Create the heatmap
ht <- Heatmap(as.matrix(sorted_data),
              name = "Log(Abundance + 1)",
              col = custom_cmap,
              show_row_names = TRUE,
              show_column_names = TRUE,
              cluster_rows = FALSE,
              cluster_columns = FALSE,
              row_names_gp = gpar(fontsize = 8),
              column_names_gp = gpar(fontsize = 8),
              heatmap_legend_param = list(
                title_gp = gpar(fontsize = 8),
                labels_gp = gpar(fontsize = 8)
              ))

# Save the heatmap
pdf("Collect/chromosome_heatmap2.pdf", width = 20, height = 5)
draw(ht)
dev.off()

print("Sorted and transposed heatmap has been generated and saved as 'chromosome_heatmap.pdf'.")
print("Log-transformed and sorted data has been saved as 'log_transformed_sorted_data.csv'.")

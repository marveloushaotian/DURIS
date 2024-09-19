# Load required libraries
library(ggplot2)
library(dplyr)
library(ggrepel)  # Add this library for non-overlapping labels

# Create a data frame with the given proportions
data <- data.frame(
  category = c("Chromosome", "Phage", "Plasmids"),
  value = c(96, 1.2, 2.8)
)

# Calculate percentages and positions for labels
data <- data %>%
  mutate(percentage = sprintf("%.1f%%", value),
         pos = cumsum(value) - 0.5 * value,
         label = paste(category, "\n", percentage))

# Create the pie chart with non-overlapping labels
pie_chart <- ggplot(data, aes(x = "", y = value, fill = category)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  geom_text_repel(aes(y = pos, label = label),
                  size = 5, fontface = "bold",
                  nudge_x = 1,
                  point.padding = NA,
                  show.legend = FALSE) +
  theme_void() +
  theme(legend.position = "none") +
  scale_fill_manual(values = c("#aa7aa7", "#beccc5", "#23496d"))

# Display the chart
print(pie_chart)

# Save the chart as PDF
ggsave("genome_composition.pdf", pie_chart, width = 8, height = 6, device = "pdf")

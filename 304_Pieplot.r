# Load required libraries
library(ggplot2)
library(dplyr)

# Data
data <- data.frame(
  Element = c('Chromosome', 'Plasmid', 'Phage'),
  Size = c(96, 2.8, 1.2)
)

# Calculate the cumulative percentages (for positioning labels)
data <- data %>%
  arrange(desc(Size)) %>%
  mutate(
    Percentage = Size / sum(Size) * 100,
    ypos = cumsum(Percentage) - 0.5 * Percentage
  )

# Create the donut chart
ggplot(data, aes(x = "", y = Size, fill = Element)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  geom_text(aes(y = ypos, label = sprintf("%.1f%%", Percentage)), color = "white", size = 5) +
  scale_fill_manual(values = c('#e3dce4', '#e1f0d6', '#dcd0dd')) +
  theme_void() +
  theme(
    legend.position = "right",
    plot.title = element_text(hjust = 0.5, size = 20, margin = margin(b = 20))
  ) +
  labs(
    title = "Distribution of Genetic Elements",
    fill = "Elements"
  ) +
  # Add a white circle in the middle to create a donut chart
  annotate("rect", xmin = -1, xmax = 1, ymin = -1, ymax = 1, fill = "white", alpha = 1) +
  xlim(-1.5, 1.5)

# Save the chart
ggsave("genetic_elements_distribution.png", width = 10, height = 10, dpi = 300)

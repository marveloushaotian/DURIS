# Load required libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(purrr)

# Read the CSV file
data <- read.csv("Results/10_Pathogen/Pathogen_Dynamic/Pathogen_Defense_Dynamic.csv")

# Reshape the data from wide to long format
data_long <- data %>%
  pivot_longer(cols = -c(Location, Country), 
               names_to = "Pathogen", 
               values_to = "Abundance")

# Select the first 6 pathogens
pathogens <- unique(data_long$Pathogen)[1:6]

# Filter data for selected pathogens
data_filtered <- data_long %>%
  filter(Pathogen %in% pathogens)

# Define colors
colors <- c("#6566aa", "#8fced1", "#75b989", "#f07e40", "#dc5772", "#969696")

# Create the plot
p <- ggplot(data_filtered, aes(x = Location, y = Abundance, color = Pathogen, group = Pathogen)) +
  geom_point(size = 3) +
  geom_line(linetype = "dashed", size = 1.2) +
  facet_wrap(~ Country, scales = "free_y", ncol = 1) +
  scale_color_manual(values = colors) +
  scale_x_discrete(limits = c("HP", "RS", "MS", "BTP")) +
  theme_bw() +
  theme(
    axis.text = element_text(size = 12, face = "bold"),
    axis.title = element_text(size = 14, face = "bold"),
    legend.text = element_text(size = 12),
    legend.title = element_text(size = 14, face = "bold"),
    strip.background = element_rect(fill = "white"),
    strip.text = element_text(size = 14, face = "bold"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.text.x = element_text(angle = 45, hjust = 1)
  ) +
  labs(
    x = NULL,
    y = "Relative Abundance",
    color = "Pathogen"
  )

# Save the plot as PDF
ggsave("defense_pathogen_abundance_plot.pdf", plot = p, width = 10, height = 15, device = cairo_pdf)

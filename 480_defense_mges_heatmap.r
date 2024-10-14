# Load required libraries
library(tidyverse)
library(ggplot2)
library(reshape2)

# Read the input file
data <- read.csv("Collect/contigs_ab_country_location_df_sing_mges_sing_with_metadata_with_defense.csv")

# Remove rows where MGEs_SubType is "No"
data <- data %>% filter(MGEs_SubType != "No")

# Count co-occurrences of Defense_Type and MGEs_SubType
co_occurrence <- data %>%
  group_by(Defense_Type, MGEs_Type, MGEs_SubType) %>%
  summarise(count = n(), .groups = 'drop') %>%
  spread(key = MGEs_SubType, value = count, fill = 0)

# Melt the data for ggplot
melted_data <- melt(co_occurrence, id.vars = c("Defense_Type", "MGEs_Type"))

# Check unique values in MGEs_Type
unique_mges_types <- unique(melted_data$MGEs_Type)
print(unique_mges_types)

# Define color palette for MGEs_Type
mges_type_colors <- c("IS" = "#E41A1C", "Prophage" = "#377EB8", "Plasmid" = "#4DAF4A",
                      "ICE" = "#984EA3", "IME" = "#FF7F00", "Other" = "#FFFF33")

# Ensure all unique MGEs_Type values have a color
for (type in unique_mges_types) {
  if (!(type %in% names(mges_type_colors))) {
    mges_type_colors[type] <- "#999999"  # Default color for unspecified types
  }
}

# Print the final color palette
print(mges_type_colors)

# Create the heatmap with original count values
ggplot(melted_data, aes(x = variable, y = Defense_Type)) +
  geom_point(aes(size = value, color = MGEs_Type), alpha = 0.7) +
  scale_size_continuous(range = c(1, 10), name = "Count") +
  scale_color_manual(values = mges_type_colors, drop = FALSE) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  ) +
  labs(title = "Co-occurrence of Defense Types and MGEs SubTypes",
       color = "MGEs Type") +
  coord_fixed()

# Save the plot
ggsave("Collect/defense_mges_co_occurrence_heatmap.pdf", width = 15, height = 15)

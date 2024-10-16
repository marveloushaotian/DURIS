library(tidyverse)
library(ggplot2)

# 1. Read the CSV file
cat("Reading input file...\n")
df <- read_csv("Collect/filtered_mge_defense_colocation_expenddf_expendmges_dedup.csv")

# 2. Filter rows where both Defense_Type and MGEs_SubType are not 'No'
filtered_df <- df %>% 
  filter(Defense_Type != 'No' & MGEs_SubType != 'No')

# 3. Create a cross-tabulation of Defense_Type and MGEs_SubType
cat("Creating cross-tabulation...\n")
cross_tab <- table(filtered_df$Defense_Type, filtered_df$MGEs_SubType)

# 4. Filter pairs with total occurrences > 10
cross_tab_filtered <- as.data.frame.matrix(cross_tab) %>%
  rownames_to_column("Defense_Type") %>%
  pivot_longer(-Defense_Type, names_to = "MGEs_SubType", values_to = "Freq") %>%
  group_by(Defense_Type, MGEs_SubType) %>%
  filter(sum(Freq) > 10) %>%
  ungroup()

# 5. Add MGEs_Type information
cross_tab_filtered <- cross_tab_filtered %>%
  left_join(filtered_df %>% select(MGEs_SubType, MGEs_Type) %>% distinct(), by = "MGEs_SubType")

# 6. Create a color palette for MGEs_Type
mge_types <- unique(cross_tab_filtered$MGEs_Type)
color_palette <- c("#6566aa", "#8fced1", "#f07e40", "#dc5772", "#7894bb", "#75b989", "#decba1")
names(color_palette) <- mge_types

# 7. Create the heatmap
cat("Generating heatmap...\n")
heatmap <- ggplot(cross_tab_filtered, aes(x = MGEs_SubType, y = Defense_Type)) +
  geom_point(aes(size = Freq, color = MGEs_Type)) +
  scale_size_continuous(range = c(1, 10)) +
  scale_color_manual(values = color_palette) +
  labs(x = '',
       y = '',
       size = 'Frequency',
       color = 'MGE Type') +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 12, face = "bold"),
    axis.text.y = element_text(size = 12, face = "bold"),
    legend.title = element_text(size = 14, face = "bold"),
    legend.text = element_text(size = 12, face = "bold"),
    legend.key.size = unit(1.5, "cm")  # Increase the size of legend keys
  ) +
  guides(size = guide_legend(override.aes = list(size = 5)))  # Increase the size of points in the legend

# 8. Save the heatmap as PDF
output_file <- "heatmap_output.pdf"
cat(sprintf("Saving heatmap to %s\n", output_file))
ggsave(output_file, heatmap, width = 15, height = 10, device = "pdf")

cat("Heatmap generation completed.\n")

# This script generates a scatter plot showing the co-occurrence frequency of Defense Types and MGE Subtypes,
# excluding rows where either is 'No' and filtering pairs with total occurrences > 10.
# The size of the points represents the frequency, and the color represents the MGE Type.
# The result is saved as a PDF file named 'heatmap_output.pdf'.

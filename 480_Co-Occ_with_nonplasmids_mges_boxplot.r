# Load required libraries
library(tidyverse)
library(ggplot2)

# Define input and output file paths
input_file <- "Collect/All_defense_info_muti.csv"
output_image <- "Results/07_Co_occ_with_Non_Plasmid_MGEs/01_Barplot_new/country_mge_defense_boxplot.pdf"
output_table <- "Results/07_Co_occ_with_Non_Plasmid_MGEs/01_Barplot_new/country_mge_defense_counts.csv"

# Define column names
element_columns <- c("Integron", "Insertion_Sequence_Type", "Transposon")
group_column <- "Country"
defense_column <- "Defense_Type"
location_column <- "Location"
sample_column <- "Sample"

# Step 1: Read data
df <- read_csv(input_file)

# Step 2: Data filtering and reshaping
filtered_df <- df %>%
  pivot_longer(cols = all_of(element_columns), 
               names_to = "Element_Type", 
               values_to = "Element_Value") %>%
  filter(!is.na(Element_Value) & Element_Value != "No") %>%
  filter(!is.na(.data[[defense_column]]) & .data[[defense_column]] != "No") %>%
  filter(!str_detect(.data[[defense_column]], paste0("^(", paste(c("PDC", "HEC", "DMS", "No"), collapse="|"), ")")))

# Step 3: Data grouping and counting
grouped_df <- filtered_df %>%
  group_by(Element_Type, .data[[group_column]], .data[[location_column]], .data[[sample_column]]) %>%
  summarise(Count = n(), .groups = "drop")

# Step 4: Adjust Location order
grouped_df[[location_column]] <- factor(grouped_df[[location_column]], 
                                        levels = c("HP", "RS", "MS", "BTP"), 
                                        ordered = TRUE)

# Step 5: Set colors
palette <- c("HP" = "#6566aa", "RS" = "#8fced1", "MS" = "#f07e40", "BTP" = "#dc5772")
 
# Step 6: Draw Boxplot
p <- ggplot(grouped_df, aes(x = .data[[group_column]], y = Count, fill = .data[[location_column]])) +
  geom_boxplot(position = position_dodge(width = 0.75)) +
  geom_jitter(position = position_jitterdodge(jitter.width = 0.2), 
              color = "black", alpha = 0.5, size = 1) +
  scale_fill_manual(values = palette) +
  theme_bw() +
  facet_wrap(~ Element_Type, scales = "free_y", ncol = 3) +  # Changed to horizontal facets
  theme(axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12, face = "bold"),
        axis.text.x = element_text(angle = 0, hjust = 0.5, size = 10),
        axis.text.y = element_text(size = 10),
        legend.position = "right",
        legend.title = element_text(size = 12, face = "bold"),
        legend.text = element_text(size = 10),
        strip.text = element_text(size = 12, face = "bold"),
        panel.grid.major = element_line(color = "gray90"),
        panel.grid.minor = element_blank(),
        panel.spacing = unit(1, "lines")) +
  labs(y = "Count", fill = "Location")

# Step 7: Save image
ggsave(output_image, p, width = 15, height = 5, dpi = 300)  # Adjusted dimensions

# Step 8: Output statistical results table
write_csv(grouped_df, output_table)

print(paste("Results saved to", output_table))
print(paste("Plot saved to", output_image))

# Load required libraries
library(tidyverse)
library(ggplot2)

# 1. Read the data
data <- read.csv("Collect/filtered_mge_defense_colocation_expenddf_expendmges.csv")

# 2. Calculate the proportion for each sample and MGEs_Type
proportion_data <- data %>%
  group_by(Country, Location, Sample, MGEs_Type) %>%
  summarise(count = sum(Defense_Type != "No" & MGEs_Type != "No"), .groups = "drop") %>%
  left_join(data %>% 
              group_by(Sample) %>% 
              summarise(total = n()), 
            by = "Sample") %>%
  mutate(proportion = count / total) %>%
  filter(MGEs_Type != "No")  # Remove rows where MGEs_Type is "No"

# 3. Create the scatter plot
ggplot(proportion_data, aes(x = Location, y = proportion, color = MGEs_Type)) +
  geom_jitter(width = 0.2, size = 3, alpha = 0.7) +
  facet_wrap(~ factor(Country, levels = c("DK", "SP", "UK")), scales = "free_x") +
  scale_x_discrete(limits = c("HS", "RS", "MS", "BTP")) +
  scale_color_manual(values = c("#6566aa", "#8fced1", "#f07e40", "#dc5772", "#7894bb", "#75b989", "#decba1")) +
  theme_bw() +
  labs(y = "% DF Co-occuring with MGE", color = "MGEs SubType") +
  theme(
    axis.text = element_text(size = 14, face = "bold"),
    axis.title = element_text(size = 16, face = "bold"),
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    axis.title.x = element_blank(),
    strip.text = element_text(size = 16, face = "bold"),
    legend.position = "right",
    legend.text = element_text(size = 12, face = "bold"),
    legend.title = element_text(size = 14, face = "bold")
  )

# 4. Save the plot
ggsave("defense_mge_proportion_scatter.pdf", width = 18, height = 10)

# Load required libraries
library(tidyverse)
library(ggplot2)

# 1. Read the data
data <- read.csv("Collect/filtered_mge_defense_colocation.csv")

# 2. Calculate the proportion for each sample
proportion_data <- data %>%
  group_by(Country, Location, Sample) %>%
  summarise(count = sum(Defense_Type != "No" & MGEs_Type != "No")) %>%
  left_join(data %>% 
              group_by(Sample) %>% 
              summarise(total = n()), 
            by = "Sample") %>%
  mutate(proportion = count / total)

# 3. Create the boxplot
ggplot(proportion_data, aes(x = Location, y = proportion, fill = Location)) +
  geom_boxplot() +
  facet_wrap(~ factor(Country, levels = c("DK", "SP", "UK")), scales = "free_x") +
  scale_fill_manual(values = c("HS" = "#6566aa", "RS" = "#8fced1", "MS" = "#f07e40", "BTP" = "#dc5772")) +
  scale_x_discrete(limits = c("HS", "RS", "MS", "BTP")) +
  theme_bw() +
  labs(y = "Proportion") +
  theme(
    axis.text = element_text(size = 12),
    axis.title = element_text(size = 14),
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    strip.text = element_text(size = 14),
    legend.position = "none"
  )

# 4. Save the plot
ggsave("defense_mge_proportion_boxplot.pdf", width = 12, height = 8)

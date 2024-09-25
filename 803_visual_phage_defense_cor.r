library(ggplot2)
library(readr)
library(dplyr)

# 1. Read the CSV file
data <- read_csv("Results/11_Phage_Defense_CoOcc/phage_defense_count.csv")  # Replace with your actual file path

# 2. Calculate correlation
correlation <- cor(data$Phage_Contigs, data$Total_Defense_Number, use = "complete.obs")

# 3. Create scatter plot with linear regression line
ggplot(data, aes(x = Phage_Contigs, y = Total_Defense_Number)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", color = "red") +
  labs(
    title = "Correlation between Phage Contigs and Total Defense Number",
    x = "Phage Contigs",
    y = "Total Defense Number",
    caption = paste("Correlation:", round(correlation, 3))
  ) +
  theme_minimal()

# 4. Save the plot
ggsave("phage_defense_correlation.pdf", width = 10, height = 8)

# 5. Print correlation coefficient
cat("Correlation coefficient:", correlation, "\n")

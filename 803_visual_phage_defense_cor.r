library(ggplot2)
library(readr)
library(dplyr)

# 1. Read the CSV file
data <- read_csv("Results/11_Phage_Defense_CoOcc/phage_defense_count.csv")  # Replace with your actual file path

# 2. Calculate correlation and p-value
cor_test <- cor.test(data$Phage_Contigs, data$Total_Defense_Number)
correlation <- cor_test$estimate
p_value <- cor_test$p.value

# 3. Create scatter plot with linear regression line
ggplot(data, aes(x = Phage_Contigs, y = Total_Defense_Number)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", color = "#dc5772") +
  labs(
    title = "Correlation between Phage Contigs and Total Defense Number",
    x = "Phage Contigs",
    y = "Total Defense Number"
  ) +
  annotate("text", x = Inf, y = Inf, 
           label = sprintf("r = %.3f\np = %.3e", correlation, p_value),
           hjust = 1.1, vjust = 1.1, size = 5, fontface = "bold") +
  theme_bw() +
  theme(
    text = element_text(size = 12, face = "bold"),
    axis.title = element_text(size = 14),
    plot.title = element_text(size = 16)
  )

# 4. Save the plot
ggsave("phage_defense_correlation.pdf", width = 8, height = 8)

# 5. Print correlation coefficient and p-value
cat("Correlation coefficient:", correlation, "\n")
cat("P-value:", p_value, "\n")

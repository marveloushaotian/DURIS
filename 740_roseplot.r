# rose plots

## All contigs classification

```{r}
library(ggplot2)

# Define data
data <- data.frame(
  group = c("CH-96%", "PL-L-PS-1.5%", "PH-1.2%","PL-L-GM-1.2%", "PL-CR-0.1%"),
  percentage = c(90, 66, 33, 33, 20)
)

# Add a minimum value to ensure small proportions are visible
data$percentage_cliff <- pmax(data$percentage, 0.1)

# Create bar plot
bar <- ggplot(data, aes(x = factor(group, levels = group), y = percentage_cliff, fill = group)) +
  geom_bar(stat = "identity", width = 1, show.legend = FALSE) +
  scale_y_continuous(limits = c(0, 100), expand = c(0, 0)) +
  scale_fill_manual(values = c("#aa7aa7","#99ce76","#ceb7ce","#d6ecc1","#75b989")) +
  theme_void() +
  labs(x = NULL, y = NULL) +
  theme(
    axis.text.y = element_blank(), 
    axis.ticks = element_blank(),
    axis.text.x = element_text(size = 12, face = "bold", color = "#333333"),
    plot.title = element_blank(),
    plot.caption = element_text(size = 10, face = "italic"),
    plot.margin = unit(c(2, 2, 2, 2), "cm")
  )

# Add polar coordinates and disable clipping
polar_bar <- bar + coord_polar(theta = "x", start = 0, clip = "off")

# Display the plot
print(polar_bar)

# Save the plot as a PDF
ggsave("rose_plot.pdf", plot = polar_bar, width = 6, height = 6, units = "in", dpi = 300)

```

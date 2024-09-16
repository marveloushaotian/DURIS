# Load required libraries
library(tidyverse)
library(ggplot2)
library(gridExtra)

# Read the input file and filter out 'Phage' entries
data <- read_csv("Results/04_DF_Correlation/correlation_original.csv") %>%
  filter(Contig_Classification != "Phage")

# Get the column names for correlation analysis (columns 10 to 76)
correlation_columns <- colnames(data)[10:76]

# Function to create a scatter plot with linear regression for each combination
create_scatter_plot <- function(data, x_var, y_var, defense_type) {
  # Calculate correlation and p-value
  cor_test <- tryCatch({
    cor.test(data[[x_var]], data[[y_var]])
  }, error = function(e) {
    return(list(estimate = NA, p.value = NA))
  })
  
  cor_value <- round(cor_test$estimate, 3)
  p_value <- cor_test$p.value
  
  # Format p-value for display
  p_value_text <- if(is.na(p_value)) {
    "p = NA"
  } else if(p_value < 0.001) {
    "p < 0.001"
  } else {
    paste("p =", round(p_value, 3))
  }
  
  # Set size values for Chromosome and Plasmid
  size_values <- c(Chromosome = 4, Plasmid = 2)
  
  # Get unique Contig_Classification values in the current subset
  unique_classifications <- unique(data$Contig_Classification)
  
  # Filter size_values to only include those present in the data
  size_values <- size_values[names(size_values) %in% unique_classifications]

  ggplot(data, aes_string(x = x_var, y = y_var)) +
    geom_point(aes(color = Location, shape = Country, alpha = factor(Season), size = Contig_Classification)) +
    geom_smooth(method = "lm", se = TRUE, color = "red", aes(group = 1)) +
    labs(title = paste("Defense Type:", defense_type),
         x = x_var, y = y_var,
         subtitle = paste("r =", if(is.na(cor_value)) "NA" else cor_value, ",", p_value_text)) +
    theme_minimal() +
    theme(plot.title = element_text(size = 12),
          plot.subtitle = element_text(size = 10),
          legend.position = "right",
          legend.box = "vertical") +
    scale_alpha_manual(values = c(0.3, 0.6, 1)) +
    scale_size_manual(values = size_values) +
    guides(color = guide_legend(override.aes = list(size=3)),
           shape = guide_legend(override.aes = list(size=3)),
           alpha = guide_legend(title = "Season", override.aes = list(size=3)),
           size = guide_legend(title = "Contig Classification", override.aes = list(size=unname(size_values))))
}

# Create and save plots for each defense type
for (defense_type in unique(data$Defense_Type)) {
  subset_data <- data %>%
    filter(Defense_Type == defense_type)
  
  plots <- lapply(correlation_columns, function(col) {
    # Filter out rows where the current column is 0
    non_zero_data <- subset_data %>% filter(!!sym(col) != 0)
    
    # Only create plot if there are more than 5 non-zero entries and correlation is significant
    if (nrow(non_zero_data) > 5) {
      cor_test <- tryCatch({
        cor.test(non_zero_data[[col]], non_zero_data$Defense_Number)
      }, error = function(e) {
        return(list(p.value = NA))
      })
      
      if (!is.na(cor_test$p.value) && cor_test$p.value < 0.05) {
        create_scatter_plot(non_zero_data, col, "Defense_Number", defense_type)
      } else {
        NULL
      }
    } else {
      NULL
    }
  })
  
  # Remove NULL elements (plots that weren't created)
  plots <- plots[!sapply(plots, is.null)]
  
  # Only proceed if there are plots to display
  if (length(plots) > 0) {
    # Arrange plots in a grid
    n_cols <- 3
    n_rows <- ceiling(length(plots) / n_cols)
    
    # Create a unique filename for each defense type
    filename <- paste0("correlation_plots_", gsub(" ", "_", defense_type), ".pdf")
    
    # Save the plot grid as a PDF
    pdf(file.path("Results/03_DF_Cor_Everything/test6", filename), width = 24, height = 8 * n_rows)
    do.call(grid.arrange, c(plots, ncol = n_cols))
    dev.off()
    
    cat("Saved plots for Defense Type:", defense_type, "as", filename, "\n")
  } else {
    cat("No significant plots created for Defense Type:", defense_type, "\n")
  }
}

cat("All significant correlation plots have been generated and saved in the 'Results/03_DF_Cor_Everything/test5' directory.\n")

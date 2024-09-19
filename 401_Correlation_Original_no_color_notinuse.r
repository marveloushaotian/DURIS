# Load required libraries
library(tidyverse)
library(ggplot2)
library(gridExtra)

# Read the input file
data <- read_csv("Results/04_DF_Correlation/correlation_original.csv")

# Get the column names for correlation analysis (columns 10 to 76)
correlation_columns <- colnames(data)[10:76]

# Function to create a scatter plot with linear regression for each combination
create_scatter_plot <- function(data, x_var, y_var, classification, defense_type) {
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
  
  ggplot(data, aes_string(x = x_var, y = y_var)) +
    geom_point(alpha = 0.5) +
    geom_smooth(method = "lm", se = TRUE, color = "red") +
    labs(title = paste(classification, "-", defense_type),
         x = x_var, y = y_var,
         subtitle = paste("r =", if(is.na(cor_value)) "NA" else cor_value, ",", p_value_text)) +
    theme_minimal() +
    theme(plot.title = element_text(size = 10),
          plot.subtitle = element_text(size = 8))
}

# Create and save plots for each combination
for (classification in unique(data$Contig_Classification)) {
  for (defense_type in unique(data$Defense_Type)) {
    subset_data <- data %>%
      filter(Contig_Classification == classification, Defense_Type == defense_type)
    
    plots <- lapply(correlation_columns, function(col) {
      # Filter out rows where the current column is 0
      non_zero_data <- subset_data %>% filter(!!sym(col) != 0)
      
      # Only create plot if there are more than 5 non-zero entries
      if (nrow(non_zero_data) > 5) {
        create_scatter_plot(non_zero_data, col, "Defense_Number", classification, defense_type)
      } else {
        NULL
      }
    })
    
    # Remove NULL elements (plots that weren't created)
    plots <- plots[!sapply(plots, is.null)]
    
    # Only proceed if there are plots to display
    if (length(plots) > 0) {
      # Arrange plots in a grid
      n_cols <- 4
      n_rows <- ceiling(length(plots) / n_cols)
      
      # Create a unique filename for each combination
      filename <- paste0("correlation_plots_", gsub(" ", "_", classification), "_", 
                         gsub(" ", "_", defense_type), ".pdf")
      
      # Save the plot grid as a PDF
      pdf(file.path("Results/03_DF_Cor_Everything/test3", filename), width = 20, height = 5 * n_rows)
      do.call(grid.arrange, c(plots, ncol = n_cols))
      dev.off()
      
      cat("Saved plots for", classification, "-", defense_type, "as", filename, "\n")
    } else {
      cat("No plots created for", classification, "-", defense_type, "(insufficient non-zero data)\n")
    }
  }
}

cat("All correlation plots have been generated and saved in the 'Results/03_DF_Cor_Everything/test2' directory.\n")

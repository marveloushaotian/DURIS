# Load required libraries
library(tidyverse)
library(ggplot2)
library(gridExtra)

# Read the input file
data <- read_csv("Results/04_DF_Correlation/correlation_original.csv")

# Get the column names for correlation analysis (columns 10 to 76)
correlation_columns <- colnames(data)[10:76]

# Function to create a scatter plot with linear regression for each combination
create_scatter_plot <- function(data, x_var, y_var, group) {
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
    labs(title = group,
         x = x_var, y = y_var,
         subtitle = paste("r =", if(is.na(cor_value)) "NA" else cor_value, ",", p_value_text)) +
    theme_minimal() +
    theme(plot.title = element_text(size = 10),
          plot.subtitle = element_text(size = 8))
}

# Function to process data and create plots for a given subset
process_subset <- function(subset_data, base_output_dir) {
  # Create a new column combining Contig_Classification and Defense_Type
  subset_data$Group <- paste(subset_data$Contig_Classification, subset_data$Defense_Type, sep = "_")
  
  for (location in unique(subset_data$Location)) {
    for (country in unique(subset_data$Country)) {
      data_subset <- subset_data %>%
        filter(Location == location, Country == country)
      
      if (nrow(data_subset) == 0) next
      
      # Create a unique directory for each Location-Country combination
      dir_name <- paste(gsub(" ", "_", location), gsub(" ", "_", country), sep = "_")
      output_dir <- file.path(base_output_dir, dir_name)
      dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
      
      for (group in unique(data_subset$Group)) {
        group_data <- data_subset %>%
          filter(Group == group)
        
        plots <- lapply(correlation_columns, function(col) {
          # Filter out rows where the current column is 0 or NA
          non_zero_data <- group_data %>% 
            filter(!is.na(!!sym(col)), !!sym(col) != 0, !is.na(Defense_Number))
          
          # Only create plot if there are more than 5 non-zero entries and correlation is significant
          if (nrow(non_zero_data) > 5) {
            cor_test <- tryCatch({
              cor.test(non_zero_data[[col]], non_zero_data$Defense_Number)
            }, error = function(e) {
              return(list(p.value = NA))
            })
            
            if (!is.na(cor_test$p.value) && cor_test$p.value < 0.05) {
              create_scatter_plot(non_zero_data, col, "Defense_Number", group)
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
          n_cols <- 4
          n_rows <- ceiling(length(plots) / n_cols)
          
          # Create a unique filename for each combination
          filename <- paste0("correlation_plots_", gsub(" ", "_", group), ".pdf")
          
          # Save the plot grid as a PDF in the Location-Country specific directory
          pdf(file.path(output_dir, filename), width = 20, height = 5 * n_rows)
          do.call(grid.arrange, c(plots, ncol = n_cols))
          dev.off()
          
          cat("Saved plots for", group, "in", location, "-", country, "as", filename, "\n")
        } else {
          cat("No significant plots created for", group, "in", location, "-", country, "\n")
        }
      }
    }
  }
}

# Process data for all combinations of Location and Country
base_output_dir <- file.path("Results/03_DF_Cor_Everything")
process_subset(data, base_output_dir)
cat("Completed processing for all Location and Country combinations\n")

cat("All significant correlation plots have been generated and saved in separate directories under '", base_output_dir, "'.\n")

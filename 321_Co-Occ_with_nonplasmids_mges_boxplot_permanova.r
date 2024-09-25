# Load required libraries
library(vegan)
library(tidyverse)

# Read the CSV file
data <- read_csv("Results/07_Co_occ_with_Non_Plasmid_MGEs/01_Barplot_new/contiglocation_mge_defense_counts.csv")
# 
# Function to perform PERMANOVA for each group
perform_permanova <- function(df, group_var) {
  results <- df %>%
    group_by(Element_Type, !!sym(group_var)) %>%
    nest() %>%
    mutate(
      permanova = map(data, ~adonis2(Count ~ Location, data = ., permutations = 999, method = "bray")),
      result = map(permanova, ~tibble(
        F_value = .$F[1],
        R2 = .$R2[1],
        p_value = .$`Pr(>F)`[1]
      ))
    ) %>%
    unnest(result) %>%
    select(-data, -permanova)
  
  return(results)
}

# Perform PERMANOVA for Contig_Classification groups
results_contig <- perform_permanova(data, "Contig_Classification")

# Perform PERMANOVA for Country groups
# results_country <- perform_permanova(data, "Country")

# Combine results
all_results <- bind_rows(
  mutate(results_contig, Group_Type = "Contig_Classification"),
  # mutate(results_country, Group_Type = "Country")
)

# Write results to CSV
write_csv(all_results, "Results/07_Co_occ_with_Non_Plasmid_MGEs/01_Barplot_new/contiglocation_mge_defense_counts_permanova.csv")

# Print summary
print(all_results)

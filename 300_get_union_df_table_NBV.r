# Load required libraries
library(dplyr)

# Define file paths
defense_path <- "Collect/overview/non_redundant_padloc.csv"

# Read defense data
defense_df <- read.csv(defense_path)

# Replace hyphens with underscores in Sample column
defense_df$Sample <- gsub("-", "_", defense_df$Sample)

# Read and process UniName data
UniName <- read.csv("Collect/01_Defense/00_DF_Name_List/Unique_defense_name.csv", header = TRUE, check.names = FALSE)
UniName_PADLOC <- UniName[,c("Unified Name","Unified Subtype Name","PADLOC Subtype Name")]
colnames(UniName_PADLOC) <- c("Unified_Name", "Unified_Subtype_Name", "SubType")

# Filter out NA and empty strings in SubType
UniName_PADLOC <- UniName_PADLOC %>% filter(!is.na(SubType) & SubType != "")

# Merge defense_df with UniName_PADLOC on 'system' and 'SubType'
defense_df <- left_join(defense_df, UniName_PADLOC, by = c("system" = "SubType"))

# Write output if do.write is TRUE
if(do.write){
  write.csv(defense_df, "Collect/overview/non_redundant_padloc_union_defense_name.csv", row.names = FALSE)
}

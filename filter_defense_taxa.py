import pandas as pd

# Read the data
df = pd.read_csv('all_defense_info_single_full_without_PDC.txt', sep='\t')

# Select the required columns
df_selected = df[['Contig_ID', 'Sample', 'Kaiju_Phylum']]

# Remove completely duplicate rows
df_unique = df_selected.drop_duplicates()

# Write the results to a new file
df_unique.to_csv('filtered_unique_rows.txt', sep='\t', index=False)

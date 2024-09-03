import pandas as pd
import argparse

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Group and calculate defense statistics.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
args = parser.parse_args()

# Load the data
df = pd.read_csv(args.input, sep='\t')

# Drop duplicate contig entries to count unique contigs
unique_contigs = df.drop_duplicates(subset='Contig_ID')

# Group by Contig_Group, Location_BAF, and Defense_Type for defense number sums
grouped_defense = df.groupby(['Contig_Group', 'Location_BAF', 'Defense_Type']).agg({
    'Defense_Num': 'sum'
}).reset_index()

# Group by Contig_Group and Location_BAF to count unique contigs
grouped_contigs = unique_contigs.groupby(['Contig_Group', 'Location_BAF']).agg({
    'Contig_ID': 'count'
}).reset_index()

# Merge the dataframes to align defense sums with unique contig counts
merged_df = pd.merge(grouped_defense, grouped_contigs, on=['Contig_Group', 'Location_BAF'])

# Calculate the GCGENOME column
merged_df['GCGENOME'] = merged_df['Defense_Num'] / merged_df['Contig_ID']

# Rename columns for clarity
merged_df.columns = ['Contig_Group', 'Location_BAF', 'Defense_Type', 'Total_Defense_Num', 'Unique_Contig_Count', 'GCGENOME']

# Save the results to a new text file
merged_df.to_csv(args.output, sep='\t', index=False)

print("Grouped statistics have been successfully saved to:", args.output)


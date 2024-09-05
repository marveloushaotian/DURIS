import pandas as pd
import argparse
from tqdm import tqdm

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Group and calculate defense statistics.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output CSV file')
args = parser.parse_args()

# Load the data
print(f"Reading input file: {args.input}")
df = pd.read_csv(args.input)

# Drop duplicate contig entries to count unique contigs
unique_contigs = df.drop_duplicates(subset='Contig_ID')

# Group by Contig_Classification, Location, and Defense_Type for defense number sums
print("Grouping and aggregating defense data...")
grouped_defense = df.groupby(['Contig_Classification', 'Location', 'Defense_Type']).agg({
    'Defense_Num': 'sum'
}).reset_index()

# Group by Contig_Classification and Location to count unique contigs
print("Grouping and counting unique contigs...")
grouped_contigs = unique_contigs.groupby(['Contig_Classification', 'Location']).agg({
    'Contig_ID': 'count'
}).reset_index()

# Merge the dataframes to align defense sums with unique contig counts
print("Merging grouped data...")
merged_df = pd.merge(grouped_defense, grouped_contigs, on=['Contig_Classification', 'Location'])

# Calculate the GCGENOME column
print("Calculating GCGENOME...")
merged_df['GCGENOME'] = merged_df['Defense_Num'] / merged_df['Contig_ID']

# Rename columns for clarity
merged_df.columns = ['Contig_Classification', 'Location', 'Defense_Type', 'Total_Defense_Num', 'Unique_Contig_Count', 'GCGENOME']

# Save the results to a new CSV file
print(f"Exporting results to: {args.output}")
merged_df.to_csv(args.output, index=False)

print(f"Grouped statistics have been successfully saved to: {args.output}")

# Usage example
print("\nUsage example:")
print("python 404_calculate_defense_gcgenome_type.py -i input_data.csv -o output_results.csv")
print("\nDescription: This script reads a CSV file containing defense system data, groups it by Contig_Classification, Location, and Defense_Type,")
print("calculates the sum of Defense_Num and count of unique Contig_ID, and computes the GCGENOME for each group.")
print("The results are then saved to a new CSV file.")

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

# Convert 'Defense_Number' to integer
df['Defense_Number'] = pd.to_numeric(df['Defense_Number'], errors='coerce').fillna(0).astype(int)

# Drop duplicate contig entries to get unique contig lengths
unique_contigs = df.drop_duplicates(subset='Contig_ID')

# Group by Contig_Classification, Location, Country, and Defense_Type
print("Grouping and aggregating data...")
grouped_defense = df.groupby(['Contig_Classification', 'Location', 'Country', 'Defense_Type']).agg({
    'Defense_Number': 'sum'
}).reset_index()

# Group by Contig_Classification, Location, and Country to get unique Contig_Length
grouped_contigs = unique_contigs.groupby(['Contig_Classification', 'Location', 'Country']).agg({
    'Contig_Length': 'sum'
}).reset_index()

# Merge the dataframes to align defense sums with contig lengths
merged_df = pd.merge(grouped_defense, grouped_contigs, on=['Contig_Classification', 'Location', 'Country'])

# Calculate the GCGB column
print("Calculating GCGB...")
merged_df['GCGB'] = (merged_df['Defense_Number'] * 1000000) / merged_df['Contig_Length']

# Rename columns for clarity
merged_df.columns = ['Contig_Classification', 'Location', 'Country', 'Defense_Type', 'Total_Defense_Num', 'Total_Contig_Length', 'GCGB']

# Save the results to a new CSV file
print(f"Exporting results to: {args.output}")
merged_df.to_csv(args.output, index=False)

print(f"Grouped statistics have been successfully saved to: {args.output}")

# Usage example
print("\nUsage example:")
print("python 402_calculate_defense_gcgb_type.py -i input_data.csv -o output_results.csv")
print("\nDescription: This script reads a CSV file containing defense system data, groups it by Contig_Classification, Location, Country, and Defense_Type,")
print("calculates the sum of Defense_Number and Contig_Length, and computes the GCGB (Gene Count per Gigabase) for each group.")
print("The results are then saved to a new CSV file.")

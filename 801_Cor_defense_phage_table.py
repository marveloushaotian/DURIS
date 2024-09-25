#!/usr/bin/env python3

import pandas as pd
import argparse
from tqdm import tqdm

def main(input_file, output_file):
    # 1. Read the input CSV file
    print("Reading input file...")
    df = pd.read_csv(input_file)

    # 2. Convert Defense_Number to numeric, replacing non-numeric values with NaN
    df['Defense_Number'] = pd.to_numeric(df['Defense_Number'], errors='coerce')

    # 3. Group by Country, Location, Sample, and Kaiju_Phylum, then count Phages
    print("Calculating Phage counts...")
    phage_counts = df.groupby(['Country', 'Location', 'Sample', 'Kaiju_Phylum'])
    phage_counts = phage_counts.apply(lambda x: (x['Contig_Classification'] == 'Phage').sum())
    phage_counts = phage_counts.reset_index(name='Phage_Count')

    # 4. Calculate defense system counts
    print("Calculating Defense system counts...")
    defense_data = df[df['Defense_Type'] != 'No']
    defense_counts = defense_data.groupby(['Country', 'Location', 'Sample', 'Defense_Type'])
    defense_counts = defense_counts['Defense_Number'].sum().reset_index(name='Defense_Sum')

    # 5. Pivot the defense counts to create wide format
    defense_wide = defense_counts.pivot(index=['Country', 'Location', 'Sample'], 
                                        columns='Defense_Type', 
                                        values='Defense_Sum').reset_index()
    defense_wide = defense_wide.fillna(0)  # Replace NaN with 0

    # 6. Combine the phage counts and defense counts
    result = pd.merge(phage_counts, defense_wide, on=['Country', 'Location', 'Sample'], how='outer')

    # 7. Display the result
    print("\nResult:")
    print(result)

    # 8. Save the result to a CSV file
    result.to_csv(output_file, index=False)
    print(f"\nResults have been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze phage counts and defense systems from contigs data.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", default="summary_result.csv", help="Output CSV file path (default: summary_result.csv)")
    args = parser.parse_args()

    main(args.input, args.output)

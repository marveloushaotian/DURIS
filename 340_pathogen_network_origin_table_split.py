import os
import pandas as pd
import argparse
from tqdm import tqdm

def filter_and_split_csv(input_file, output_dir):
    # 1. Read the input CSV file
    df = pd.read_csv(input_file)

    # 2. Filter out rows where 'Defense_Type' starts with 'PDC_', 'HEC_', or 'DMS_other'
    df_filtered = df[~df['Defense_Type'].str.startswith(('PDC_', 'HEC_', 'DMS_other'))]

    # 3. Filter out rows where 'Contig_Classification' is 'Phage'
    df_filtered = df_filtered[df_filtered['Contig_Classification'] != 'Phage']

    # 4. Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 5. Group by 'Location', 'Country', and 'Contig_Classification' and save each group to a separate CSV file
    grouped = df_filtered.groupby(['Location', 'Country', 'Contig_Classification'])
    for (location, country, contig_classification), group in tqdm(grouped, desc="Processing groups"):
        output_file = os.path.join(output_dir, f"{location}_{country}_{contig_classification}.csv")
        group.to_csv(output_file, index=False)
        print(f"Processed file saved: {output_file}")

def main():
    # 6. Set up argument parser
    parser = argparse.ArgumentParser(description="Filter and split CSV file based on 'Location', 'Country', and 'Contig_Classification' columns.")
    parser.add_argument('-i', '--input_file', type=str, required=True, help="Input CSV file")
    parser.add_argument('-o', '--output_dir', type=str, required=True, help="Output directory to save the split CSV files")
    args = parser.parse_args()

    # 7. Filter and split the CSV file
    filter_and_split_csv(args.input_file, args.output_dir)

if __name__ == "__main__":
    main()

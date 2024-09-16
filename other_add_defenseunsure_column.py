import pandas as pd
import argparse
from tqdm import tqdm

def process_defense_data(input_file, output_file):
    # 1. Read the input CSV file
    df = pd.read_csv(input_file)

    # 2. Add Defense_Unsure column with progress bar
    tqdm.pandas(desc="Processing Defense_Type")
    df['Defense_Unsure'] = df['Defense_Type'].progress_apply(lambda x: 'Yes' if str(x).startswith('PDC_') else 'No')

    # 3. Save to output CSV file
    df.to_csv(output_file, index=False)
    print(f"Defense_Unsure column has been added and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Defense_Unsure column based on Defense_Type")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path")
    args = parser.parse_args()

    process_defense_data(args.input, args.output)

# Usage example:
# python defenseunsure.py -i all_defense_info_single_full.csv -o all_defense_info_single_full_updated.csv

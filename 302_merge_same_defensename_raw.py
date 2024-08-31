import argparse
import pandas as pd
from tqdm import tqdm

def merge_and_sum_rows(input_file, output_file):
    """
    Merges rows based on the first column and sums up the values of the other columns.
    """
    print("Reading input file.")
    df = pd.read_csv(input_file, sep='\t', dtype={0: str})
    
    print("Processing data.")
    # Group by the first column and sum the other columns
    grouped_df = df.groupby(df.columns[0]).sum().reset_index()

    print("Writing output file.")
    grouped_df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge rows based on the first column and sum values of other columns.')
    parser.add_argument('-i', '--input', required=True, help='Input .txt file path.')
    parser.add_argument('-o', '--output', required=True, help='Output .txt file path.')
    args = parser.parse_args()

    print('Script started.')
    merge_and_sum_rows(args.input, args.output)
    print('Script finished.')

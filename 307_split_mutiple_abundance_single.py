import pandas as pd
import argparse
from tqdm import tqdm

def process_csv(input_file, output_file):
    # 1. Read the input CSV file
    df = pd.read_csv(input_file)
    
    # 2. Split the Defense_Type column and expand the dataframe
    df_expanded = df.assign(Defense_Type=df['Defense_Type'].str.split(';')).explode('Defense_Type')
    
    # 3. Group by Defense_Type and sum the values of other columns
    df_grouped = df_expanded.groupby('Defense_Type').sum().reset_index()
    
    # 4. Save the result to a new CSV file
    df_grouped.to_csv(output_file, index=False)
    print(f"Processed file saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Process CSV file by splitting Defense_Type column and grouping.')
    parser.add_argument('-i', '--input', required=True, help='Path to input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Path to output CSV file')
    args = parser.parse_args()
    
    print("Starting CSV processing...")
    process_csv(args.input, args.output)
    print("CSV processing completed successfully.")

if __name__ == "__main__":
    main()

# Usage example:
# python script_name.py -i path/to/input.csv -o path/to/output.csv
#
# This script processes a CSV file by splitting the Defense_Type column on semicolons,
# creating new rows for each split value, and then grouping by Defense_Type while
# summing the values in other columns. The result is saved to a new CSV file.

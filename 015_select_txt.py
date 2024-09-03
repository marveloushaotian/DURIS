import argparse
import pandas as pd
from tqdm import tqdm

def select_and_export(input_file, output_file, column_filters):
    # Step 1: Read the input file
    print("Reading input file...")
    df = pd.read_csv(input_file, sep='\t')

    # Step 2: Apply filters
    print("Applying filters...")
    for column, values in column_filters.items():
        df = df[df[column].isin(values)]

    # Step 3: Export to new file
    print("Exporting to new file...")
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Exported {len(df)} rows to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Select rows from a tab-separated file based on specific values in specified columns.")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output file path")
    parser.add_argument('-f', '--filters', nargs='+', required=True, help="Filters in the format 'column:value1,value2,...'")
    args = parser.parse_args()

    # Parse filters
    column_filters = {}
    for f in args.filters:
        column, values = f.split(':')
        column_filters[column] = values.split(',')

    select_and_export(args.input, args.output, column_filters)

if __name__ == "__main__":
    main()

# Usage example:
# python script_name.py -i input.txt -o output.txt -f "Contig_Group:MG_chr" "Sample:Sample_01,Sample_02"
#
# This script reads a tab-separated file, selects rows based on specified values
# in the given columns, and exports the result to a new tab-separated file.
# Progress information is printed to the console.
# 
# Parameters:
# -i, --input: Input file path (required)
# -o, --output: Output file path (required)
# -f, --filters: Filters in the format "column:value1,value2,..." (one or more) (required)
#                You can specify multiple filters for different columns.

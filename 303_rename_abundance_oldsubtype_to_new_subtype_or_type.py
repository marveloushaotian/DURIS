import os
import pandas as pd
import argparse
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description='Replace row names in CSV files, merge rows with the same name, remove specific rows, and remove rows with all zeros.')
    parser.add_argument('-i', '--input_dir', required=True, help='Input directory containing CSV files to process')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory for saving processed CSV files')
    parser.add_argument('-m', '--mapping_file', required=True, help='CSV file containing mapping for row name replacement')
    parser.add_argument('-s', '--subtype_column', default='Defense_Subtype', help='Column name in mapping file for subtypes (default: Defense_Subtype)')
    parser.add_argument('-t', '--type_column', default='Defense_Type', help='Column name in mapping file for types (default: Defense_Type)')
    return parser.parse_args()

def process_file(input_file, output_file, mapping_dict):
    # Read the input CSV file
    df = pd.read_csv(input_file, index_col=0)
    
    # Replace '-' with '_' in row names
    df.index = df.index.str.replace('-', '_')
    
    # Replace row names using the mapping dictionary
    df.index = df.index.map(lambda x: mapping_dict.get(x, x))
    
    # Group by the new index and sum the values
    df = df.groupby(df.index).sum()
    
    # Remove rows starting with HEC_, PDC_, and DMS_other
    df = df[~df.index.str.match(r'^(HEC_|PDC_|DMS_other)')]
    
    # Remove rows where all values are zero
    df = df.loc[(df != 0).any(axis=1)]
    
    # Save the processed dataframe to a new CSV file
    df.to_csv(output_file)

def main():
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Read the mapping file
    mapping_df = pd.read_csv(args.mapping_file)
    mapping_dict = dict(zip(mapping_df[args.subtype_column], mapping_df[args.type_column]))
    
    # Process all CSV files in the input directory
    for filename in tqdm(os.listdir(args.input_dir), desc="Processing files"):
        if filename.endswith('.csv'):
            input_file = os.path.join(args.input_dir, filename)
            output_file = os.path.join(args.output_dir, f"processed_{filename}")
            process_file(input_file, output_file, mapping_dict)
    
    print("All files have been processed and saved in the output directory.")

if __name__ == "__main__":
    main()
import pandas as pd
import argparse

def main(input_file, output_file):
    # Read the input file
    df = pd.read_csv(input_file)
    
    # Extract Sample and Phylum columns
    df_extracted = df[['Sample', 'Phylum']]
    
    # Create pivot table with Samples as columns, Phylums as rows, and counts as values
    pivot_table = df_extracted.pivot_table(index='Phylum', columns='Sample', aggfunc='size', fill_value=0)
    
    # Save to new file
    pivot_table.to_csv(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a table with Samples as columns and Phylums as rows, with counts as values")
    parser.add_argument('-i', '--input', required=True, help="Input file path (CSV format)")
    parser.add_argument('-o', '--output', required=True, help="Output file path (CSV format)")
    
    args = parser.parse_args()
    main(args.input, args.output)

#!/usr/bin/env python3

import argparse
import csv
from tqdm import tqdm

def process_kaiju_output(input_file, output_file, target_column, filter_value='C'):
    """
    Process Kaiju output file and filter results based on specified criteria.
    
    Args:
    input_file (str): Path to the input CSV file
    output_file (str): Path to the output CSV file
    target_column (str): Name of the column to process (e.g., 'Kaiju_Class')
    filter_value (str): Value to filter rows by in the first column (default: 'C')
    """
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header
        writer.writerow(['Contig_ID', target_column])
        
        # Process rows
        for row in tqdm(reader, desc="Processing rows"):
            if row[0] == filter_value:
                contig_id = row[1]
                target_value = row[3].strip().replace(' ', '_')
                target_value = 'No' if target_value == 'NA' else target_value
                writer.writerow([contig_id, target_value])

def main():
    parser = argparse.ArgumentParser(description="Process Kaiju output and filter results.")
    parser.add_argument('-i', '--input', required=True, help="Input CSV file path")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file path")
    parser.add_argument('-c', '--column', default='Kaiju_Class', help="Target column name (default: Kaiju_Class)")
    parser.add_argument('-f', '--filter', default='C', help="Filter value for the first column (default: C)")
    args = parser.parse_args()

    process_kaiju_output(args.input, args.output, args.column, args.filter)

if __name__ == "__main__":
    main()

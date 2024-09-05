import argparse
import csv
from pathlib import Path
from tqdm import tqdm
import os

def convert_tsv_to_csv(input_file, output_file):
    """
    Convert a tab-separated (TSV) file to a comma-separated (CSV) file.
    
    Args:
        input_file (str): Path to the input TSV file
        output_file (str): Path to the output CSV file
    """
    with open(input_file, 'r', newline='') as tsv_file, \
         open(output_file, 'w', newline='') as csv_file:
        
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        csv_writer = csv.writer(csv_file)
        
        # Use tqdm to show progress
        total_lines = sum(1 for _ in open(input_file))
        for row in tqdm(tsv_reader, total=total_lines, desc="Converting"):
            csv_writer.writerow(row)

def process_files(input_path, output_path):
    # Create output directory if it doesn't exist
    if os.path.isdir(input_path):
        os.makedirs(output_path, exist_ok=True)
    elif not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.isfile(input_path) and not os.path.isdir(output_path):
        # Process single file
        convert_tsv_to_csv(input_path, output_path)
    elif os.path.isdir(input_path) and os.path.isdir(output_path):
        # Process directory
        for tsv_file in input_path.glob('*.txt'):
            csv_file = output_path / tsv_file.with_suffix('.csv').name
            convert_tsv_to_csv(tsv_file, csv_file)
    else:
        raise ValueError("Input and output must be both files or both directories.")

def main():
    parser = argparse.ArgumentParser(description="Convert tab-separated (TSV) files to comma-separated (CSV) files.")
    parser.add_argument("-i", "--input", required=True, help="Input TSV file or directory path")
    parser.add_argument("-o", "--output", help="Output CSV file or directory path (default: input_name.csv or input_dir_csv)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not args.output:
        if input_path.is_file():
            output_path = input_path.with_suffix('.csv')
        else:
            output_path = input_path.with_name(f"{input_path.name}_csv")
    else:
        output_path = Path(args.output)

    process_files(input_path, output_path)
    print(f"Conversion complete. Output: {output_path}")

if __name__ == "__main__":
    main()

# Usage examples:
# python script_name.py -i input.txt -o output.csv
# python script_name.py -i input_dir -o output_dir
# For help: python script_name.py -h

# Sample dataset (save as 'sample.txt'):
"""
Name\tAge\tCity
John\t30\tNew York
Alice\t25\tLos Angeles
Bob\t35\tChicago
"""

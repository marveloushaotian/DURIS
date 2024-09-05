import argparse
import csv
from pathlib import Path
from tqdm import tqdm

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

def main():
    parser = argparse.ArgumentParser(description="Convert a tab-separated (TSV) file to a comma-separated (CSV) file.")
    parser.add_argument("-i", "--input", required=True, help="Input TSV file path")
    parser.add_argument("-o", "--output", help="Output CSV file path (default: input_file_name.csv)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not args.output:
        output_path = input_path.with_suffix('.csv')
    else:
        output_path = Path(args.output)

    convert_tsv_to_csv(input_path, output_path)
    print(f"Conversion complete. Output file: {output_path}")

if __name__ == "__main__":
    main()

# Usage example:
# python script_name.py -i input.txt -o output.csv
# For help: python script_name.py -h

# Sample dataset (save as 'sample.txt'):
"""
Name\tAge\tCity
John\t30\tNew York
Alice\t25\tLos Angeles
Bob\t35\tChicago
"""

#!/usr/bin/env python3
import argparse
import csv
import logging
from pathlib import Path
from tqdm import tqdm
import os

def convert_csv_to_tsv(input_file, output_file):
    """
    Convert a CSV file to a TSV file.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output TSV file
    """
    with open(input_file, 'r', newline='') as csvfile, \
         open(output_file, 'w', newline='') as tsvfile:
        csv_reader = csv.reader(csvfile)
        tsv_writer = csv.writer(tsvfile, delimiter='\t')
        
        for row in csv_reader:
            tsv_writer.writerow(row)

def process_input(input_path, output_dir):
    """
    Process input files or directory and convert CSV to TSV.
    
    Args:
        input_path (Path): Path to input file or directory
        output_dir (Path): Path to output directory
    """
    if input_path.is_file():
        if input_path.suffix.lower() == '.csv':
            output_file = output_dir / (input_path.stem + '.txt')
            convert_csv_to_tsv(str(input_path), str(output_file))
            logging.info(f"Converted {input_path} to {output_file}")
    elif input_path.is_dir():
        csv_files = list(input_path.glob('*.csv'))
        for file in tqdm(csv_files, desc="Converting files"):
            output_file = output_dir / (file.stem + '.txt')
            convert_csv_to_tsv(str(file), str(output_file))
            logging.info(f"Converted {file} to {output_file}")
        
        if not csv_files:
            logging.warning(f"No CSV files found in the directory: {input_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert CSV file(s) to TSV file(s)")
    parser.add_argument('-i', '--input', required=True, help="Input CSV file or directory containing CSV files")
    parser.add_argument('-o', '--output', help="Output directory for TSV files (default: same as input)")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    input_path = Path(args.input)
    if not input_path.exists():
        logging.error(f"Input path not found: {input_path}")
        return

    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = input_path.parent if input_path.is_file() else input_path
    
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Processing input: {input_path}")
    process_input(input_path, output_dir)
    logging.info("Conversion completed successfully")

if __name__ == "__main__":
    main()

# Usage examples:
# python script.py -i input.csv -o output_dir
# python script.py -i input_directory
# python script.py -i input_directory -o output_directory
# python script.py -h  # For help

import argparse
import os
import csv
from tqdm import tqdm

def merge_files(input_files, output_file, file_type):
    delimiter = '\t' if file_type == 'txt' else ','
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=delimiter)
        for i, input_file in enumerate(tqdm(input_files, desc="Merging Files")):
            with open(input_file, 'r', newline='') as infile:
                reader = csv.reader(infile, delimiter=delimiter)
                if i == 0:
                    for row in reader:
                        writer.writerow(row)
                else:
                    next(reader)  # Skip header
                    for row in reader:
                        writer.writerow(row)

def collect_files(input_paths, file_type):
    all_files = []
    for path in input_paths:
        if os.path.isdir(path):
            for file in os.listdir(path):
                if file.endswith(f'.{file_type}'):
                    all_files.append(os.path.join(path, file))
        elif os.path.isfile(path) and path.endswith(f'.{file_type}'):
            all_files.append(path)
    return all_files

def main():
    parser = argparse.ArgumentParser(
        description='Merge multiple text or CSV files into one. Accepts files and directories.',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Example: %(prog)s -i file1.txt dir1 file2.txt -o merged_output.txt -t txt'
    )
    parser.add_argument('-i', '--input', type=str, nargs='+', required=True,
                        help='Input files or directories to merge. Usage: -i file1.txt dir1 ...')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file to save the merged content.')
    parser.add_argument('-t', '--type', type=str, choices=['txt', 'csv'], required=True,
                        help='File type to process (txt or csv)')
    args = parser.parse_args()

    input_files = collect_files(args.input, args.type)

    if not input_files:
        print(f'Error: No valid {args.type} files found to merge.')
        return

    merge_files(input_files, args.output, args.type)
    print('Merge completed successfully.')

if __name__ == '__main__':
    main()

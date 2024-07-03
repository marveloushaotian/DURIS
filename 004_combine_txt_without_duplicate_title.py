import argparse
import logging
import os
from tqdm import tqdm

# Setup logging
logging.basicConfig(filename='merge_txt_files.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def merge_files(input_files, output_file):
    """
    Merges multiple text files into one with specific rules.
    The first file is included entirely, subsequent files skip the first line.

    Args:
    - input_files (list): List of paths to the input files.
    - output_file (str): Path to the output file.
    """
    with open(output_file, 'w') as outfile:
        for i, input_file in enumerate(tqdm(input_files, desc="Merging Files")):
            with open(input_file, 'r') as infile:
                if i == 0:
                    # Copy the first file in its entirety
                    outfile.write(infile.read())
                else:
                    # Skip the first line for subsequent files
                    next(infile)
                    outfile.write(infile.read())
            logging.info(f'Processed {input_file}')

def collect_files(input_paths):
    """
    Collects all text files from the provided paths. If a path is a directory,
    all text files in the directory are collected.

    Args:
    - input_paths (list): List of file or directory paths.

    Returns:
    - list: List of text file paths.
    """
    all_files = []
    for path in input_paths:
        if os.path.isdir(path):
            # List all text files in the directory
            for file in os.listdir(path):
                if file.endswith('.txt'):
                    all_files.append(os.path.join(path, file))
        elif os.path.isfile(path) and path.endswith('.txt'):
            all_files.append(path)
    return all_files

def main():
    parser = argparse.ArgumentParser(description='Merge multiple text files into one. Accepts files and directories.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', type=str, nargs='+', required=True,
                        help='Input text files or directories to merge. Usage: -i file1.txt dir1 ...')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file to save the merged content.')
    args = parser.parse_args()

    # Collect all files to be merged
    input_files = collect_files(args.input)

    if not input_files:
        logging.error('No valid text files found to merge.')
        print('Error: No valid text files found to merge.')
        return

    # Merge the files
    merge_files(input_files, args.output)
    logging.info('Merge completed successfully.')

if __name__ == '__main__':
    main()


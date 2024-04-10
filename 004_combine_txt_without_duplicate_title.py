import argparse
import logging
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

def main():
    parser = argparse.ArgumentParser(description='Merge multiple text files into one.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', type=str, nargs='+', required=True,
                        help='Input text files to merge. Usage: -i file1.txt file2.txt ...')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file to save the merged content.')
    args = parser.parse_args()

    # Merge the files
    merge_files(args.input, args.output)
    logging.info('Merge completed successfully.')

if __name__ == '__main__':
    main()


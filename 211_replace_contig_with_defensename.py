import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_files(input_file, reference_file, output_file):
    # Step 1: Read the input file and filter rows
    logging.info("Reading input file...")
    df = pd.read_csv(input_file, sep="\t", header=None)

    # Remove rows where the first column ends with 'sort_filter.bam' or is 'Unknown'
    df = df[~df[0].str.endswith('sort_filter.bam')]
    df = df[df[0] != 'Unknown']

    # Step 2: Read the reference file
    logging.info("Reading reference file...")
    ref_df = pd.read_csv(reference_file, sep="\t", header=None)

    # Create a dictionary from the reference file for quick lookup
    ref_dict = dict(zip(ref_df[2], ref_df[3]))

    # Step 3: Replace the matching entries in the input file
    logging.info("Replacing matching entries...")
    df[0] = df[0].apply(lambda x: ref_dict.get(x, x))

    # Step 4: Save the result to the output file
    logging.info("Saving the result to the output file...")
    df.to_csv(output_file, sep="\t", header=False, index=False)
    logging.info("Process completed successfully.")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process and filter a txt file.")
    parser.add_argument("-i", "--input", required=True, help="Input txt file")
    parser.add_argument("-r", "--reference", required=True, help="Reference txt file")
    parser.add_argument("-o", "--output", required=True, help="Output txt file")

    args = parser.parse_args()

    # Run the process
    process_files(args.input, args.reference, args.output)


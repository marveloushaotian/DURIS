import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_files(input_file, reference_file, output_file):
    # Step 1: Read the input file and filter rows
    logging.info("Reading input file...")
    df = pd.read_csv(input_file, sep="\t", low_memory=False)

    # Remove rows where the first column ends with 'sort_filter.bam' or is 'Unknown'
    df = df[~df.iloc[:, 0].str.endswith('sort_filter.bam')]
    df = df[df.iloc[:, 0] != 'Unknown']

    # Step 2: Read the reference file
    logging.info("Reading reference file...")
    ref_df = pd.read_csv(reference_file, sep="\t", header=None)

    # Create a dictionary from the reference file for quick lookup
    ref_dict = dict(zip(ref_df[2], ref_df[3]))

    # Step 3: Replace the matching entries in the input file
    logging.info("Replacing matching entries...")
    df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: ref_dict.get(x, x))

    # Step 4: Combine rows with the same first column and sum the values
    logging.info("Combining rows and summing values...")
    numeric_cols = df.columns[1:]  # All columns except the first one
    combined_df = df.groupby(df.columns[0], as_index=False)[numeric_cols].sum()

    # Step 5: Save the result to the output file
    logging.info("Saving the result to the output file...")
    combined_df.to_csv(output_file, sep="\t", index=False)
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


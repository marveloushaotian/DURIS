import argparse
import pandas as pd
from tqdm import tqdm
import logging

# Setup logging
logging.basicConfig(filename='process_seqs.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_file(input_file, output_file):
    """
    Process the input file to extract the full sequence IDs (excluding '>') and lengths, 
    then save them to the output file in CSV format.
    """
    logging.info("Starting processing.")
    try:
        data = []  # List to hold the extracted data
        with open(input_file, 'r') as file:
            for line in tqdm(file, desc="Processing lines"):
                if line.startswith('>'):
                    # Remove the leading '>' and find the 'length' and its following number
                    clean_line = line[1:].strip()
                    length = clean_line.split('_length_')[1].split('_')[0]
                    data.append({'seqid': clean_line, 'length': length})

        # Convert the list to a DataFrame and save as CSV
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        logging.info("Processing completed successfully.")
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Extract sequence IDs and lengths from a file.")
    parser.add_argument('-i', '--input', help="Input file path", required=True)
    parser.add_argument('-o', '--output', help="Output CSV file path", required=True)
    
    args = parser.parse_args()
    
    process_file(args.input, args.output)

if __name__ == "__main__":
    main()


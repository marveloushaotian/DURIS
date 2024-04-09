import argparse
import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='update_column_names.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def update_column_names(input_file, output_file):
    """
    Updates column names by extracting the third element and prepending it with 'Sample_'.
    """
    logging.info("Reading input file.")
    df = pd.read_csv(input_file, sep='\t', header=0)
    
    # Extract and update column names starting from the second column
    new_columns = [df.columns[0]]  # Keep the first column name as is
    for col in df.columns[1:]:
        # Split the column name and extract the third item
        third_item = col.split('-')[2]
        new_columns.append('Sample_' + third_item)

    df.columns = new_columns

    logging.info("Writing output file.")
    df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and update column names in a tab-separated .txt file.')
    parser.add_argument('-i', '--input', required=True, help='Input .txt file path.')
    parser.add_argument('-o', '--output', required=True, help='Output .txt file path.')
    args = parser.parse_args()

    logging.info('Script started.')
    update_column_names(args.input, args.output)
    logging.info('Script finished.')


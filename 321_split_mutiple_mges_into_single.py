import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def split_mges_info(input_file, output_file):
    # Load the data
    logging.info(f'Loading data from {input_file}')
    df = pd.read_csv(input_file)
    
    # Expand rows based on semicolon-separated values in 'MGEs_Type' and 'MGEs_SubType'
    logging.info('Splitting rows based on semicolon-separated values in MGEs_Type and MGEs_SubType')
    expanded_rows = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        mges_types = row['MGEs_Type'].split(';')
        mges_subtypes = row['MGEs_SubType'].split(';')
        if len(mges_types) != len(mges_subtypes):
            raise ValueError(f'Mismatched lengths for MGEs_Type and MGEs_SubType in row {index}')
        for mt, mst in zip(mges_types, mges_subtypes):
            new_row = row.copy()
            new_row['MGEs_Type'] = mt.strip()
            new_row['MGEs_SubType'] = mst.strip()
            expanded_rows.append(new_row)
    
    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows)
    
    # Save the expanded DataFrame to a new file
    logging.info(f'Saving expanded data to {output_file}')
    expanded_df.to_csv(output_file, index=False)
    logging.info('Done!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split MGEs info by MGEs_Type and MGEs_SubType columns.')
    parser.add_argument('-i', '--input', required=True, help='Input file path (MGEs_info.csv)')
    parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    split_mges_info(args.input, args.output)

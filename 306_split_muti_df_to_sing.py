import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def split_defense_info(input_file, output_file):
    # Load the data
    logging.info(f'Loading data from {input_file}')
    df = pd.read_csv(input_file)
    
    # Expand rows based on semicolon-separated values in 'Defense_Type' and 'Defense_Subtype'
    logging.info('Splitting rows based on semicolon-separated values in Defense_Type and Defense_Subtype')
    expanded_rows = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        defense_types = row['Defense_Type'].split(';')
        defense_subtypes = row['Defense_Subtype'].split(';')
        if len(defense_types) != len(defense_subtypes):
            raise ValueError(f'Mismatched lengths for Defense_Type and Defense_Subtype in row {index}')
        for dt, dst in zip(defense_types, defense_subtypes):
            new_row = row.copy()
            new_row['Defense_Type'] = dt.strip()
            new_row['Defense_Subtype'] = dst.strip()
            expanded_rows.append(new_row)
    
    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows)
    
    # Save the expanded DataFrame to a new file
    logging.info(f'Saving expanded data to {output_file}')
    expanded_df.to_csv(output_file, index=False)
    logging.info('Done!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split All_defense_info.csv by Defense_Type and Defense_Subtype columns.')
    parser.add_argument('-i', '--input', required=True, help='Input file path (All_defense_info.csv)')
    parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    split_defense_info(args.input, args.output)

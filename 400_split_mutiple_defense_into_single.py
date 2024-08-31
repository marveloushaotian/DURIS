import pandas as pd
import argparse
from tqdm import tqdm

def split_defense_info(input_file, output_file):
    # Load the data
    print(f'Loading data from {input_file}')
    df = pd.read_csv(input_file, sep='\t')

    # Ensure Defense_Type and Defense_Subtype columns are strings and fill NaN values with empty strings
    df['Defense_Type'] = df['Defense_Type'].astype(str).fillna('')
    df['Defense_Subtype'] = df['Defense_Subtype'].astype(str).fillna('')

    # Expand rows based on comma-separated values in 'Defense_Type' and 'Defense_Subtype'
    print('Splitting rows based on comma-separated values in Defense_Type and Defense_Subtype')
    expanded_rows = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        defense_types = row['Defense_Type'].split(',')
        defense_subtypes = row['Defense_Subtype'].split(',')
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
    print(f'Saving expanded data to {output_file}')
    expanded_df.to_csv(output_file, sep='\t', index=False)
    print('Done!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split All_defense_info.txt by Defense_Type and Defense_Subtype columns.')
    parser.add_argument('-i', '--input', required=True, help='Input file path (All_defense_info.txt)')
    parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    split_defense_info(args.input, args.output)

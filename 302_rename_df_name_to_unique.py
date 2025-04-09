import pandas as pd
import argparse
from tqdm import tqdm

def process_defense_info(all_defense_file, unique_defense_file, output_file):
    # Step 1: Read the CSV files
    all_defense_df = pd.read_csv(all_defense_file)
    unique_defense_df = pd.read_csv(unique_defense_file)

    # Step 2: Create a mapping dictionary for Defense_Type and Defense_Subtype
    type_mapping = dict(zip(unique_defense_df['Defense_Type'], unique_defense_df['Defense_Type_Inuse']))
    subtype_mapping = dict(zip(unique_defense_df['Defense_Subtype'], unique_defense_df['Defense_Subtype_Inuse']))

    # Step 3: Apply the mapping to all_defense_df
    all_defense_df['Defense_Type_Inuse'] = all_defense_df['Defense_Type'].map(type_mapping)
    all_defense_df['Defense_Subtype_Inuse'] = all_defense_df['Defense_Subtype'].map(subtype_mapping)

    # Step 4: Drop the original Defense_Type and Defense_Subtype columns
    all_defense_df = all_defense_df.drop(columns=['Defense_Type', 'Defense_Subtype'])

    # Step 5: Rename the new columns
    all_defense_df = all_defense_df.rename(columns={
        'Defense_Type_Inuse': 'Defense_Type',
        'Defense_Subtype_Inuse': 'Defense_Subtype'
    })

    # Step 6: Save the processed dataframe to a new CSV file
    all_defense_df.to_csv(output_file, index=False)
    print(f"Processed file saved as {output_file}")

def main():
    # Hardcoded path for unique defense file
    unique_defense_file = 'Collect/03_Defense/00_DF_Name_List/unique_defense_name.csv'
    
    files_to_process = [
        ('Collect/03_Defense/01_DF_Full_Table/all_defense_info_mutiple.csv', 'Collect/03_Defense/01_DF_Full_Table/processed_all_defense_info_mutiple.csv'),
        ('Collect/03_Defense/01_DF_Full_Table/all_defense_info_single.csv', 'Collect/03_Defense/01_DF_Full_Table/processed_all_defense_info_single.csv')
    ]

    for input_file, output_file in tqdm(files_to_process, desc="Processing files"):
        process_defense_info(input_file, unique_defense_file, output_file)

if __name__ == "__main__":
    main()

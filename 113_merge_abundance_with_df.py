import pandas as pd
from tqdm import tqdm

def merge_defense_info(input_file1, input_file2, output_file):
    """
    Merge defense information from two CSV files based on Contig_ID.
    
    Args:
        input_file1 (str): Path to contigs_ab_country_location_allinfo.csv
        input_file2 (str): Path to All_defense_info_muti.csv
        output_file (str): Path to save the merged result
    """
    # 1. Read input files
    print("Reading input files...")
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)
    
    # 2. Merge dataframes
    print("Merging dataframes...")
    merged_df = pd.merge(df1, 
                         df2[['Contig_ID', 'Defense_Type', 'Defense_Subtype', 'Defense_Number']], 
                         on='Contig_ID', 
                         how='left')
    
    # 3. Fill NaN values with 'No'
    print("Filling missing values...")
    merged_df['Defense_Type'] = merged_df['Defense_Type'].fillna('No')
    merged_df['Defense_Subtype'] = merged_df['Defense_Subtype'].fillna('No')
    merged_df['Defense_Number'] = merged_df['Defense_Number'].fillna('No')
    
    # 4. Save merged result
    print("Saving merged result...")
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved as {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Merge defense information from two CSV files based on Contig_ID.")
    parser.add_argument('-i1', '--input1', required=True, help="Path to contigs_ab_country_location_allinfo.csv")
    parser.add_argument('-i2', '--input2', required=True, help="Path to All_defense_info_muti.csv")
    parser.add_argument('-o', '--output', required=True, help="Path to save the merged result")
    
    args = parser.parse_args()
    
    merge_defense_info(args.input1, args.input2, args.output)

# Usage example:
# python script_name.py -i1 contigs_ab_country_location_allinfo.csv -i2 All_defense_info_muti.csv -o merged_result.csv

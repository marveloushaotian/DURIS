import pandas as pd
from tqdm import tqdm

def merge_contig_info(file1, file2, output_file):
    """
    Merge contig information from two CSV files based on Contig_ID.
    
    Args:
    -i1: Path to the first input CSV file (contigs_ab_country_location.csv)
    -i2: Path to the second input CSV file (All_contigs_info_muti_defense.csv)
    -o: Path to the output CSV file
    
    Example:
    python script.py -i1 contigs_ab_country_location.csv -i2 All_contigs_info_muti_defense.csv -o merged_contig_info.csv
    """
    # 1. Read the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # 2. Define columns to merge from df2
    columns_to_merge = [
        'Contig_Group', 'Contig_Classification', 'Contig_Length', 'Inc',
        'Mobility', 'Integron', 'Insertion_Sequence_Type', 'Transposon',
        'ARGs',
        'COG_Category', 'COG_Num', 'Kaiju_Kingdom', 'Kaiju_Phylum',
        'Kaiju_Class', 'Kaiju_Order', 'Kaiju_Family', 'Kaiju_Genus',
        'Kaiju_Species'
    ]
    
    # 3. Merge dataframes
    merged_df = pd.merge(df1, df2[['Contig_ID'] + columns_to_merge], on='Contig_ID', how='left')
    
    # 4. Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved as {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Merge contig information from two CSV files based on Contig_ID.")
    parser.add_argument('-i1', required=True, help="Path to the first input CSV file (contigs_ab_country_location.csv)")
    parser.add_argument('-i2', required=True, help="Path to the second input CSV file (All_contigs_info_muti_defense.csv)")
    parser.add_argument('-o', required=True, help="Path to the output CSV file")
    
    args = parser.parse_args()
    
    merge_contig_info(args.i1, args.i2, args.o)

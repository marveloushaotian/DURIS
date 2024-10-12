import pandas as pd
import argparse
from tqdm import tqdm

def analyze_defense_and_abundance(input_csv, abundance_csv, output_csv):
    # 1. Read input CSV files
    df = pd.read_csv(input_csv)
    abundance_df = pd.read_csv(abundance_csv, index_col=0)
    
    # 2. Filter df based on Contig_Group values
    valid_contig_groups = ['MG_chr', 'MG_phage', 'MG_pls_circ', 'MG_pls_lin_gm', 'MG_pls_lin_pl']
    df = df[df['Contig_Group'].isin(valid_contig_groups)]
    
    # 3. Group by Sample and count Defense_Type
    defense_counts = df.groupby('Sample')['Defense_Type'].count().reset_index()
    defense_counts.columns = ['Sample', 'Defense_Count']
    
    # 4. Calculate Phage abundance for each Sample
    abundance_sums = abundance_df.sum().reset_index()
    abundance_sums.columns = ['Sample', 'Phage_Abundance']
    
    # 5. Merge Defense_Count and Phage_Abundance
    result_df = pd.merge(defense_counts, abundance_sums, on='Sample', how='outer')
    
    # 6. Check for unmatched samples
    unmatched_defense = set(defense_counts['Sample']) - set(abundance_sums['Sample'])
    unmatched_abundance = set(abundance_sums['Sample']) - set(defense_counts['Sample'])
    
    if unmatched_defense or unmatched_abundance:
        print("Warning: Some samples did not match between the two input files.")
        print(f"Samples in defense file but not in abundance file: {unmatched_defense}")
        print(f"Samples in abundance file but not in defense file: {unmatched_abundance}")
    
    # 7. Save to CSV
    result_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
    print(f"Total matched samples: {len(result_df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze defense types and phage abundance.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path with Defense_Type data')
    parser.add_argument('-a', '--abundance', required=True, help='Input CSV file path with phage abundance data')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')
    args = parser.parse_args()

    analyze_defense_and_abundance(args.input, args.abundance, args.output)

# Usage example:
# python script_name.py -i input_defense.csv -a input_abundance.csv -o output_results.csv

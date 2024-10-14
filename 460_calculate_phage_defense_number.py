import pandas as pd
import argparse
from tqdm import tqdm

def analyze_defense_types(input_file, output_file):
    # 1. Read CSV file
    df = pd.read_csv(input_file)
    
    # 2. Group by Location, Country, and Sample
    grouped = df.groupby(['Location', 'Country', 'Sample'])
    
    results = []
    
    # 3. Analyze each group
    for name, group in tqdm(grouped, desc="Analyzing groups"):
        location, country, sample = name
        
        # Calculate Phage proportion and counts
        total_contigs = group.shape[0]
        phage_contigs = group[group['Contig_Classification'] == 'Phage'].shape[0]
        phage_proportion = phage_contigs / total_contigs if total_contigs > 0 else 0
        
        # Calculate total Defense_Number (excluding 'No')
        total_defense_number = group[group['Defense_Number'] != 'No']['Defense_Number'].astype(float).sum()
        
        result = {
            'Location': location,
            'Country': country,
            'Sample': sample,
            'Total_Contigs': total_contigs,
            'Phage_Contigs': phage_contigs,
            'Phage_Proportion': phage_proportion,
            'Total_Defense_Number': total_defense_number
        }
        
        results.append(result)
    
    # 4. Create result DataFrame
    result_df = pd.DataFrame(results)
    
    # 5. Save to CSV
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze defense types in contigs.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')
    args = parser.parse_args()

    analyze_defense_types(args.input, args.output)

# Import required libraries
import pandas as pd
import argparse
from pathlib import Path

def analyze_plasmid_defense(input_file, output_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Filter for Plasmid contigs
    plasmid_df = df[df['Contig_Classification'] == 'Plasmid']
    
    # Group by Location, Country, and Mobility
    grouped = plasmid_df.groupby(['Location', 'Country', 'Mobility'])
    
    # Calculate statistics
    results = []
    for name, group in grouped:
        total_count = len(group)
        defense_count = len(group[group['Defense_Type'] != 'No'])
        defense_ratio = defense_count / total_count if total_count > 0 else 0
        
        results.append({
            'Location': name[0],
            'Country': name[1],
            'Mobility': name[2],
            'Total_Plasmids': total_count,
            'Plasmids_with_Defense': defense_count,
            'Defense_Ratio': defense_ratio
        })
    
    # Create result DataFrame and save to CSV
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze plasmid defense systems.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path")
    args = parser.parse_args()

    analyze_plasmid_defense(args.input, args.output)

# Usage example:
# python script_name.py -i input_file.csv -o output_file.csv

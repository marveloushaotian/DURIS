import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from itertools import combinations
import argparse
from tqdm import tqdm

def perform_anova(data, loc1, loc2):
    group1 = data[data['Location'] == loc1]['GCGB']
    group2 = data[data['Location'] == loc2]['GCGB']
    
    # Perform one-way ANOVA
    f_value, p_value = f_oneway(group1, group2)
    
    return f_value, p_value

def main(input_file, output_file):
    # Read the CSV data
    df = pd.read_csv(input_file)

    # Initialize results dictionary
    results = {}

    # Perform ANOVA for each combination
    for contig_class in tqdm(df['Contig_Classification'].unique(), desc="Processing Contig Classifications"):
        results[contig_class] = {}
        for country in df['Country'].unique():
            results[contig_class][country] = {}
            
            # Filter data
            filtered_data = df[(df['Contig_Classification'] == contig_class) & 
                               (df['Country'] == country)]
            
            # Get unique locations for this combination
            locations = filtered_data['Location'].unique()
            
            # Perform pairwise ANOVA
            for loc1, loc2 in combinations(locations, 2):
                pair_data = filtered_data[filtered_data['Location'].isin([loc1, loc2])]
                try:
                    f_value, p_value = perform_anova(pair_data, loc1, loc2)
                    results[contig_class][country][(loc1, loc2)] = {
                        'F-value': f_value,
                        'p-value': p_value
                    }
                except ValueError:
                    # This will catch cases where there's not enough data for the analysis
                    results[contig_class][country][(loc1, loc2)] = {
                        'F-value': 'N/A',
                        'p-value': 'N/A'
                    }

    # Create a DataFrame from the results
    result_rows = []
    for contig_class in results:
        for country in results[contig_class]:
            for loc_pair in results[contig_class][country]:
                result_rows.append({
                    'Contig_Classification': contig_class,
                    'Country': country,
                    'Location_Pair': f"{loc_pair[0]} vs {loc_pair[1]}",
                    'F-value': results[contig_class][country][loc_pair]['F-value'],
                    'p-value': results[contig_class][country][loc_pair]['p-value']
                })

    result_df = pd.DataFrame(result_rows)

    # Save results to CSV
    result_df.to_csv(output_file, index=False)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform ANOVA analysis on GCGB data.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')
    args = parser.parse_args()

    main(args.input, args.output)

# Usage example:
# python 403_permanova_statisitc.py -i Results/09_Test/test_sample_order.csv -o anova_results_real.csv
import pandas as pd
import numpy as np
from scipy import stats
from tqdm import tqdm

def read_data(file_path, index_col):
    return pd.read_csv(file_path, index_col=index_col)

def calculate_correlations(df1, df2, alpha=0.05, correlation_threshold=0.7):
    results = []
    total_comparisons = len(df1.index) * len(df2.index)
    with tqdm(total=total_comparisons, desc="Calculating correlations") as pbar:
        for item1 in df1.index:
            for item2 in df2.index:
                # Ensure columns are aligned before calculating correlation
                common_columns = df1.columns.intersection(df2.columns)
                if len(common_columns) > 0:
                    x = df1.loc[item1, common_columns]
                    y = df2.loc[item2, common_columns]
                    r, p = stats.spearmanr(x, y)  # Changed to Spearman correlation
                    if p < alpha and (r > correlation_threshold or r < -correlation_threshold):
                        direction = 'Positive' if r > 0 else 'Negative'
                        results.append((item1, item2, r, p, direction))
                pbar.update(1)
    return results

# 1. Read data
defense_df = read_data('top31_Defense_Type_abundance_percentage_all_samples.csv', 'Defense_Type')
phylum_df = read_data('top31_Kaiju_Phylum_abundance_percentage_all_samples.csv', 'Kaiju_Phylum')
phage_df = read_data('top31_Phage_Family_abundance_percentage_all_samples.csv', 'Phage_Family')

# 2. Calculate correlations
defense_phylum = calculate_correlations(defense_df, phylum_df)
defense_phage = calculate_correlations(defense_df, phage_df)
phylum_phage = calculate_correlations(phylum_df, phage_df)

# 3. Create results DataFrame
results_df = pd.DataFrame(defense_phylum + defense_phage + phylum_phage, 
                          columns=['Item1', 'Item2', 'Correlation', 'P-value', 'Direction'])

# 4. Add comparison type column
results_df['Comparison'] = results_df.apply(lambda row: 'Defense-Phylum' if row['Item1'] in defense_df.index and row['Item2'] in phylum_df.index else
                                            ('Defense-Phage' if row['Item1'] in defense_df.index and row['Item2'] in phage_df.index else 'Phylum-Phage'), axis=1)

# 5. Sort results
results_df = results_df.sort_values('Correlation', ascending=False)

# 6. Save results to CSV file
output_file = 'correlation_results.csv'
results_df.to_csv(output_file, index=False)

print(results_df)

# Usage example:
# python calculate_correlation.py
#
# This script calculates Spearman correlations between defense types, phyla, and phage families.
# It considers correlations significant if p < 0.05 and |r| > 0.7.
# The script ensures that corresponding columns are matched when calculating correlations.
# Results are saved to 'correlation_results.csv'.

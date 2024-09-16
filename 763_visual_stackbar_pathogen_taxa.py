import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from tqdm import tqdm

def process_csv(input_file, output_file):
    # 1. Read the CSV file
    df = pd.read_csv(input_file)
    
    # 2. Filter species with more than 20 entries
    species_counts = df['Kaiju_Species'].value_counts()
    species_to_keep = species_counts[species_counts > 20].index
    filtered_df = df[df['Kaiju_Species'].isin(species_to_keep)]
    
    # 3. Get top 8 defense types for each species
    def get_top_8_defenses(group):
        top_8 = group['Defense_Type'].value_counts().nlargest(8)
        return group[group['Defense_Type'].isin(top_8.index)]
    
    top_8_df = filtered_df.groupby('Kaiju_Species').apply(get_top_8_defenses).reset_index(drop=True)
    
    # 4. Create a stacked bar plot
    plt.figure(figsize=(50, 25))  # Increased figure size
    species_order = filtered_df['Kaiju_Species'].value_counts().index
    
    # Calculate Defense_Type counts for each species
    defense_type_counts = top_8_df.groupby(['Kaiju_Species', 'Defense_Type']).size().unstack(fill_value=0)
    
    # Plot stacked bar chart
    ax = defense_type_counts.loc[species_order].plot(kind='bar', stacked=True)
    
    plt.title('Top 8 Defense Types by Kaiju Species', fontsize=20)
    plt.xlabel('Kaiju Species', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.legend(title='Defense Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    
    # Rotate x-axis labels and adjust their position
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout to prevent cutting off labels
    plt.tight_layout()
    
    # Adjust subplot to make room for x-axis labels
    plt.subplots_adjust(bottom=0.2)
    
    # 5. Save the plot with higher DPI
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV and create stacked bar plot of Top 8 Defense Types by Kaiju Species.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output image file path")
    args = parser.parse_args()

    process_csv(args.input, args.output)

print("Processing complete. Stacked bar plot of top 8 defense types saved.")

# Usage example:
# python stackbar_pathogen_taxa.py -i input.csv -o output.png

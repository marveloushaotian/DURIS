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
    
    # 3. Filter out unwanted defense types
    filtered_df = filtered_df[~filtered_df['Defense_Type'].str.startswith(('PDC', 'HEC', 'DMS', 'No'))]
    
    # 4. Get top 5 defense types for each species
    def get_top_5_defenses(group):
        top_5 = group['Defense_Type'].value_counts().nlargest(5)
        return group[group['Defense_Type'].isin(top_5.index)]
    
    top_5_df = filtered_df.groupby('Kaiju_Species').apply(get_top_5_defenses).reset_index(drop=True)
    
    # 5. Create a stacked bar plot
    plt.figure(figsize=(50, 25))  # Increased figure size
    species_order = filtered_df['Kaiju_Species'].value_counts().index
    
    # Calculate Defense_Type counts for each species
    defense_type_counts = top_5_df.groupby(['Kaiju_Species', 'Defense_Type']).size().unstack(fill_value=0)
    
    # Define color palette with 40 distinct colors
    color_palette = [
        "#c0dbe6", "#2b526f", "#4a9ba7", "#a3cbd6", "#c0cfbd", "#9bb88a", "#7b9b64", "#d0cab7",
        "#c6a4c5", "#9b7baa", "#7a7aaf", "#434d91", "#5284a2", "#82b4c8", "#9d795d", "#d1b49a",
        "#fff08c", "#e1834e", "#cd6073", "#ffc7c9", "#969696", "#d1d9e2", "#ff6b6b", "#4ecdc4",
        "#45b7d1", "#f7dc6f", "#f39c12", "#8e44ad", "#3498db", "#1abc9c", "#2ecc71", "#e74c3c",
        "#34495e", "#95a5a6", "#d35400", "#c0392b", "#7f8c8d", "#bdc3c7", "#16a085", "#27ae60"
    ]
    
    # Plot stacked bar chart with custom colors
    ax = defense_type_counts.loc[species_order].plot(kind='bar', stacked=True, color=color_palette)
    
    plt.title('Top 5 Defense Types by Kaiju Species', fontsize=20)
    plt.xlabel('Kaiju Species', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.legend(title='Defense Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    
    # Rotate x-axis labels and adjust their position
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout to prevent cutting off labels
    plt.tight_layout()
    
    # Adjust subplot to make room for x-axis labels
    plt.subplots_adjust(bottom=0.2)
    
    # 6. Save the plot with higher DPI
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV and create stacked bar plot of Top 5 Defense Types by Kaiju Species.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output image file path")
    args = parser.parse_args()

    process_csv(args.input, args.output)

print("Processing complete. Stacked bar plot of top 5 defense types saved.")

# Usage example:
# python stackbar_pathogen_taxa.py -i input.csv -o output.png

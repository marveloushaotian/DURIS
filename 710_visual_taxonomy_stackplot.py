import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def process_data(df, filter_defense=False):
    # Filter out empty or 'No' values in Kaiju_Phylum
    df = df[df['Kaiju_Phylum'].notna() & (df['Kaiju_Phylum'] != 'No')]
    
    if filter_defense:
        df = df[df['Defense_Type'].notna() & (df['Defense_Type'] != 'No')]
    
    # Group by Country, Location, and Kaiju_Phylum
    grouped = df.groupby(['Country', 'Location', 'Kaiju_Phylum']).size().unstack(fill_value=0)
    
    # Calculate percentages
    percentages = grouped.div(grouped.sum(axis=1), axis=0) * 100
    
    # Sort columns by total percentage (descending) and keep top 20
    sorted_cols = percentages.sum().sort_values(ascending=False)
    top_20 = sorted_cols.head(20).index.tolist()
    
    # Combine remaining phyla into 'Others'
    percentages['Others'] = percentages.loc[:, ~percentages.columns.isin(top_20)].sum(axis=1)
    percentages = percentages[top_20 + ['Others']]
    
    # Sort columns by total abundance (descending)
    sorted_cols = percentages.sum().sort_values(ascending=False)
    percentages = percentages[sorted_cols.index]
    
    return percentages

def plot_stacked_bar(data, title, output_file):
    colors = ["#c0dbe6","#2b526f","#4a9ba7","#a3cbd6","#c0cfbd","#9bb88a","#7b9b64","#d0cab7","#c6a4c5","#9b7baa","#7a7aaf","#434d91","#5284a2","#82b4c8","#9d795d","#d1b49a","#fff08c","#e1834e","#cd6073","#ffc7c9","#969696","#d1d9e2"]
    
    # Create a figure with subplots for each country
    countries = data.index.get_level_values('Country').unique()
    fig, axes = plt.subplots(1, len(countries), figsize=(20, 8), sharey=True)
    fig.suptitle(title, fontsize=20, fontweight='bold')
    
    for i, country in enumerate(countries):
        country_data = data.loc[country]
        
        # Ensure the order of locations is HP, RS, MS, BTP
        location_order = ['HP', 'RS', 'MS', 'BTP']
        country_data = country_data.reindex(location_order)
        
        country_data.plot(kind='bar', stacked=True, ax=axes[i], color=colors[:len(country_data.columns)], width=0.4)
        
        axes[i].set_title(country, fontsize=16, fontweight='bold')
        axes[i].set_xlabel('')
        if i == 0:
            axes[i].set_ylabel('Abundance of Taxonomy', fontsize=14, fontweight='bold')
        axes[i].tick_params(axis='both', which='major', labelsize=12)
        axes[i].set_xticklabels(axes[i].get_xticklabels(), fontweight='bold')
        
        # Rotate x-axis labels and align them to the center of the bars
        plt.setp(axes[i].get_xticklabels(), rotation=0, ha='center')
        
        # Remove individual legends
        axes[i].get_legend().remove()
        
        # Reduce space between bars
        axes[i].margins(x=0.01)
    
    # Add a common legend
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles[::-1], labels[::-1], loc='center right', bbox_to_anchor=(1.1, 0.5), fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved as {output_file}")

def main(input_file, output_prefix):
    # Read the data
    df = pd.read_csv(input_file)
    
    # Process data for both charts
    data_all = process_data(df)
    data_defense = process_data(df, filter_defense=True)
    
    # Ensure consistent legend for both charts
    all_phyla = set(data_all.columns) | set(data_defense.columns)
    data_all = data_all.reindex(columns=all_phyla, fill_value=0)
    data_defense = data_defense.reindex(columns=all_phyla, fill_value=0)
    
    # Create the plots
    plot_stacked_bar(data_all, 'All Contigs', f"{output_prefix}_all_contigs.png")
    plot_stacked_bar(data_defense, 'Contigs with Defense Systems', f"{output_prefix}_defense_contigs.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stacked bar charts from contig data")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_prefix", help="Prefix for output chart files")
    args = parser.parse_args()
    
    main(args.input_file, args.output_prefix)

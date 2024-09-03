import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def process_data(df, filter_defense=False):
    # Filter out empty or 'No' values in Kaiju_Phylum
    df = df[df['Kaiju_Phylum'].notna() & (df['Kaiju_Phylum'] != 'No')]
    
    if filter_defense:
        df = df[df['Defense_Type'].notna() & (df['Defense_Type'] != 'No')]
    
    # Group by Country, Location_BAF, and Kaiju_Phylum
    grouped = df.groupby(['Country', 'Location_BAF', 'Kaiju_Phylum']).size().unstack(fill_value=0)
    
    # Calculate percentages
    percentages = grouped.div(grouped.sum(axis=1), axis=0) * 100
    
    # Sort columns by total percentage (descending) and keep top 20
    sorted_cols = percentages.sum().sort_values(ascending=False)
    top_20 = sorted_cols.head(20).index.tolist()
    
    # Combine remaining phyla into 'Others'
    percentages['Others'] = percentages.loc[:, ~percentages.columns.isin(top_20)].sum(axis=1)
    percentages = percentages[top_20 + ['Others']]
    
    return percentages

def plot_stacked_bar(ax, data, title):
    colors = ["#c0dbe6","#2b526f","#4a9ba7","#a3cbd6","#c0cfbd","#9bb88a","#7b9b64","#d0cab7","#c6a4c5","#9b7baa","#7a7aaf","#434d91","#5284a2","#82b4c8","#9d795d","#d1b49a","#fff08c","#e1834e","#cd6073","#ffc7c9","#969696","#d1d9e2"]
    
    data.plot(kind='bar', stacked=True, ax=ax, color=colors, width=0.8)
    
    ax.set_title(title)
    ax.set_xlabel('')
    ax.set_ylabel('Percentage')
    ax.legend().remove()
    
    # Rotate x-axis labels and align them to the center of the bars
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
    
    # Replace 'Before_Filter' with 'BF' and 'After_Filter' with 'AF' in x-axis labels
    labels = [item.get_text().replace('Before_Filter', 'BF').replace('After_Filter', 'AF') for item in ax.get_xticklabels()]
    ax.set_xticklabels(labels)

def main(input_file, output_file):
    # Read the data
    df = pd.read_csv(input_file, sep='\t')
    
    # Process data for both charts
    data_all = process_data(df)
    data_defense = process_data(df, filter_defense=True)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    plot_stacked_bar(ax1, data_all, 'All Data')
    plot_stacked_bar(ax2, data_defense, 'Filtered by Defense Type')
    
    # Add a common legend
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles[::-1], labels[::-1], loc='center right', bbox_to_anchor=(1.1, 0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stacked bar charts from contig data")
    parser.add_argument("input_file", help="Path to the input TSV file")
    parser.add_argument("output_file", help="Path to save the output chart")
    args = parser.parse_args()
    
    main(args.input_file, args.output_file)

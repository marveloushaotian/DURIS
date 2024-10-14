import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import numpy as np

def process_data(df, contig_class):
    # Filter data based on Contig_Classification
    df_filtered = df[df['Contig_Classification'] == contig_class]
    
    # Filter out empty or 'No' values in Kaiju_Phylum
    df_filtered = df_filtered[df_filtered['Kaiju_Phylum'].notna() & (df_filtered['Kaiju_Phylum'] != 'No')]
    
    # Define the desired order for Location
    location_order = ['HP', 'RS', 'MS', 'BTP']
    
    # Group by Country, Location, and Kaiju_Phylum
    grouped = df_filtered.groupby(['Country', 'Location', 'Kaiju_Phylum']).size().unstack(fill_value=0)
    
    # Sort the index based on Country and the custom Location order
    grouped = grouped.reset_index()
    grouped['Location'] = pd.Categorical(grouped['Location'], categories=location_order, ordered=True)
    grouped = grouped.sort_values(['Country', 'Location']).set_index(['Country', 'Location'])
    
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
    # colors = ["#c0dbe6","#2b526f","#4a9ba7","#a3cbd6","#c0cfbd","#9bb88a","#7b9b64","#d0cab7","#c6a4c5","#9b7baa","#7a7aaf","#434d91","#5284a2","#82b4c8","#9d795d","#d1b49a","#fff08c","#e1834e","#cd6073","#ffc7c9","#969696","#d1d9e2"]
    
    colors = ["#6566aa","#c6a4c5","#c6f0ec","#8fced1","#53a4a6",
              "#d0cab7","#c0dbe6","#509d95","#75b989","#92ca77",
              "#d6ecc1","#e7ee9f","#f7ded5","#faaf7f","#f07e40",
              "#dc5772","#ebc1d1","#f9e7e7","#decba1","#d4888b",
              "#969696","#d1d9e2"]

    # Sort columns by total percentage (descending)
    sorted_cols = data.sum().sort_values(ascending=False).index.tolist()
    data_sorted = data[sorted_cols]
    
    # Plot stacked bars
    data_sorted.plot(kind='bar', stacked=True, ax=ax, color=colors, width=0.8)
    
    ax.set_title(title)
    ax.set_xlabel('')
    ax.set_ylabel('Percentage')
    ax.legend().remove()
    
    # Rotate x-axis labels and align them to the center of the bars
    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
    
    # Replace 'Before_Filter' with 'BF' and 'After_Filter' with 'AF' in x-axis labels
    labels = [f"{country}\n{loc}" for country, loc in data_sorted.index]
    ax.set_xticklabels(labels)
    
    # Remove space at the top of the bars
    ax.set_ylim(0, 100)
    
    # Increase spacing between countries
    ax.set_xticklabels(ax.get_xticklabels(), ha='center')
    ax.tick_params(axis='x', which='major', pad=10)
    
    # Add extra space between countries
    country_breaks = np.cumsum([len(data[data.index.get_level_values('Country') == country]) 
                                for country in data.index.get_level_values('Country').unique()])
    for break_point in country_breaks[:-1]:
        ax.axvline(break_point - 0.5, color='white', linewidth=2)
    
    return sorted_cols

def main(input_file, output_file):
    # Read the data in CSV format
    df = pd.read_csv(input_file)
    
    # Get unique Contig_Classification values
    contig_classes = df['Contig_Classification'].unique()
    
    # Create a figure with 3 subplots side by side
    fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    
    # Process data and create plots for each Contig_Classification
    sorted_cols_list = []
    for ax, contig_class in zip(axes, contig_classes):
        data = process_data(df, contig_class)
        sorted_cols = plot_stacked_bar(ax, data, f'Contig Classification: {contig_class}')
        sorted_cols_list.append(sorted_cols)
    
    # Add a common legend with order based on abundance
    handles, labels = axes[-1].get_legend_handles_labels()
    sorted_labels = sorted_cols_list[-1]  # Use the order from the last subplot
    sorted_handles = [handles[labels.index(label)] for label in sorted_labels]
    fig.legend(sorted_handles, sorted_labels, loc='center right', bbox_to_anchor=(1.3, 0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stacked bar charts from contig data")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to save the output chart")
    args = parser.parse_args()
    
    main(args.input_file, args.output_file)

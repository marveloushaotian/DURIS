import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import numpy as np

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

    percentages.reset_index(inplace=True)
    
    return percentages

def plot_stacked_bar(ax, data, title):
    # Ensure 'Country' and 'Location' are columns
    if isinstance(data.index, pd.MultiIndex):
        data = data.reset_index()
    elif 'Country' not in data.columns or 'Location' not in data.columns:
        data = data.reset_index()
    
    # Get unique countries and locations
    location_order = ['HP', 'RS', 'MS', 'BTP']
    countries = data['Country'].unique()
    
    # Initialize variables
    current_x = 0
    gap_between_countries = 1.3  # Increase this value for larger gaps
    width = 0.7
    x_positions = []
    x_labels = []
    position_mapping = {}
    
    # Assign x positions
    for country in countries:
        country_data = data[data['Country'] == country]
        # Ensure locations are in the desired order
        country_data = country_data.set_index('Location').reindex(location_order).dropna(subset=['Country']).reset_index()
        num_locations = len(country_data)
        positions = current_x + np.arange(num_locations)
        for idx, row in country_data.iterrows():
            loc = row['Location']
            position = positions[idx - country_data.index[0]]
            position_mapping[(country, loc)] = position
            x_positions.append(position)
            x_labels.append(f"{country}\n{loc}")
        current_x = positions[-1] + gap_between_countries  # Add gap between countries
    
    # Map x positions back to data
    data['x_pos'] = data.apply(lambda row: position_mapping.get((row['Country'], row['Location']), np.nan), axis=1)
    
    # Plot the data
    phyla_cols = [col for col in data.columns if col not in ['Country', 'Location', 'x_pos']]
    bottom = np.zeros(len(data))
    # colors = ["#c0dbe6", "#2b526f", "#4a9ba7", "#a3cbd6", "#c0cfbd", "#9bb88a", "#7b9b64", "#d0cab7",
    #           "#c6a4c5", "#9b7baa", "#7a7aaf", "#434d91", "#5284a2", "#82b4c8", "#9d795d", "#d1b49a",
    #           "#fff08c", "#e1834e", "#cd6073", "#ffc7c9", "#969696", "#d1d9e2"]
    
    colors = ["#6566aa","#c6a4c5","#c6f0ec","#8fced1","#53a4a6",
              "#d0cab7","#c0dbe6","#509d95","#75b989","#92ca77",
              "#d6ecc1","#e7ee9f","#f7ded5","#faaf7f","#f07e40",
              "#dc5772","#ebc1d1","#f9e7e7","#decba1","#d4888b",
              "#969696","#d1d9e2"]

    for idx, phylum in enumerate(phyla_cols):
        values = data[phylum].values
        ax.bar(data['x_pos'], values, width=width, bottom=bottom, color=colors[idx % len(colors)], label=phylum)
        bottom += values
    
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=90, ha='center')
    ax.set_title(title)
    ax.set_ylabel('Abundance of Taxonomy (%)')
    ax.margins(x=0.02)
    ax.set_ylim(0, 100)  # Set y-axis limit to 100%

def main(input_file, output_file):
    # Read the data
    df = pd.read_csv(input_file)
    
    # Process data for both charts
    data_all = process_data(df)
    data_defense = process_data(df, filter_defense=True)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    plot_stacked_bar(ax1, data_all, 'All Data')
    plot_stacked_bar(ax2, data_defense, 'Filtered by Defense Type')
    
    # Add a common legend
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc='center right', bbox_to_anchor=(1.3, 0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stacked bar charts from contig data")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to save the output chart")
    args = parser.parse_args()
    
    main(args.input_file, args.output_file)

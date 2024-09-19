import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import numpy as np

def create_stacked_bar_chart(input_file, output_file, value_column):
    # Step 1: Load the data
    df = pd.read_csv(input_file)

    # Step 2: Calculate the total proportion of each Defense_Type across all groups
    total_proportion = df.groupby('Defense_Type')[value_column].sum()
    top_defense_types = total_proportion.nlargest(20).index

    # Step 3: Filter the dataframe to retain only the top 20 defense types
    filtered_df = df[df['Defense_Type'].isin(top_defense_types)]

    # Step 4: Define custom colors
    custom_colors = ["#c0dbe6","#2b526f","#4a9ba7","#a3cbd6","#c0cfbd","#9bb88a","#7b9b64","#d0cab7","#c6a4c5","#9b7baa",
                     "#7a7aaf","#434d91","#5284a2","#82b4c8","#9d795d","#d1b49a","#fff08c","#e1834e","#cd6073","#ffc7c9",
                     "#969696","#d1d9e2"]
    color_dict = dict(zip(top_defense_types, custom_colors[:len(top_defense_types)]))

    # Step 5: Create subplots for each Contig_Classification and Country
    contig_classifications = filtered_df['Contig_Classification'].unique()
    countries = filtered_df['Country'].unique()
    
    fig, axes = plt.subplots(1, len(contig_classifications) * len(countries), figsize=(28, 7), sharex=False, sharey=False)

    # Increase font size for all text elements
    plt.rcParams.update({'font.size': 14, 'font.weight': 'bold'})

    subplot_index = 0
    for contig_classification in contig_classifications:
        for country in countries:
            ax = axes[subplot_index]
            class_country_df = filtered_df[(filtered_df['Contig_Classification'] == contig_classification) & (filtered_df['Country'] == country)]
            
            # Group by Location
            locations = class_country_df['Location'].unique()
            
            # Create a new DataFrame for plotting
            plot_data = pd.DataFrame(index=locations, columns=top_defense_types, dtype=np.float64)
            
            for location in locations:
                location_df = class_country_df[class_country_df['Location'] == location]
                for defense_type in top_defense_types:
                    value = location_df[location_df['Defense_Type'] == defense_type][value_column].sum()
                    plot_data.loc[location, defense_type] = value if value > 0 else 0.0
            
            # Plot the stacked bar chart with reduced width and spacing
            plot_data.plot(kind='bar', stacked=True, ax=ax, width=0.8, color=[color_dict[col] for col in plot_data.columns], legend=False)
            
            # Adjust bar positions to reduce spacing
            for container in ax.containers:
                plt.setp(container, width=0.8)
            
            # Adjust x-axis limits to reduce spacing between bars
            ax.set_xlim(-0.5, len(locations) - 0.5)
            
            # Remove x-axis ticks
            ax.tick_params(axis='x', which='both', bottom=False, top=False)
            
            ax.set_xticklabels(locations, rotation=0, ha='center', fontsize=12, fontweight='bold')
            ax.set_xlabel('', fontsize=18, fontweight='bold')
            if subplot_index == 0:  # Only set y-label for the leftmost subplot
                ax.set_ylabel('Defense Abundance', fontsize=14, fontweight='bold')
            else:
                ax.set_ylabel('', fontsize=14, fontweight='bold')
            ax.set_title(f'{contig_classification}\n{country}', fontsize=16, fontweight='bold')
            
            subplot_index += 1

    # Add a single legend for all subplots, removing duplicates
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend = fig.legend(by_label.values(), by_label.keys(), title='Defense Type', bbox_to_anchor=(1.01, 0.5), loc='center left', ncol=1, fontsize=12, frameon=False)
    legend.get_title().set_fontsize(14)  # Increase font size for legend title
    legend.get_title().set_fontweight('bold')  # Make legend title bold
    plt.setp(legend.get_texts(), fontsize=12, fontweight='bold')  # Increase font size and make bold for legend text

    # Adjust spacing between legend items
    legend._loc = 2  # upper left
    legend._ncol = 1  # single column
    legend._bbox_to_anchor = (1.01, 1)  # move it closer to the left
    legend.set_bbox_to_anchor((1.01, 0.5))
    legend._loc = 6  # center left

    plt.tight_layout(rect=[0, 0, 0.98, 1])  # Adjust the right margin to make the plot more compact
    plt.savefig(output_file, format='pdf', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Create a stacked bar chart by Contig Classification, Country, and Location for top 20 defense types.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
    parser.add_argument('-v', '--value', type=str, required=True, help='Name of the column to be used as value (e.g., GCGENOME)')
    
    args = parser.parse_args()

    create_stacked_bar_chart(args.input, args.output, args.value)

if __name__ == '__main__':
    main()

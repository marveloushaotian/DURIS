import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use Agg backend, which may help resolve some rendering issues
import matplotlib.pyplot as plt
import argparse
from matplotlib import gridspec

def create_stacked_bar_chart(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Filter out rows with Defense_Type starting with PDC, HEC, DMS, or equal to 'No'
    df = df[~df['Defense_Type'].str.startswith(('PDC', 'HEC', 'DMS')) & (df['Defense_Type'] != 'No')]
    
    # Group by Defense_Type and Contig_Classification
    grouped = df.groupby(['Defense_Type', 'Contig_Classification']).size().unstack(fill_value=0)
    
    # Sort Defense_Types by total count
    total_counts = grouped.sum(axis=1).sort_values(ascending=False)
    grouped = grouped.loc[total_counts.index]
    
    # Define custom colors for the chart
    custom_colors = ["#4a9ba7", "#9bb88a", "#d0cab7", "#c6a4c5", "#434d91", "#e1834e", "#cd6073", "#ffc7c9"]
    
    # Create figure with two subplots
    fig = plt.figure(figsize=(20, 12))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4])
    
    ax_top = plt.subplot(gs[0])
    ax_bottom = plt.subplot(gs[1])
    
    # Plot the stacked bar chart for both subplots
    grouped.plot(kind='bar', stacked=True, color=custom_colors, edgecolor='black', linewidth=0.5, ax=ax_top)
    grouped.plot(kind='bar', stacked=True, color=custom_colors, edgecolor='black', linewidth=0.5, ax=ax_bottom)
    
    # Set y-axis limits for the top subplot (4000 to 6000)
    ax_top.set_ylim(1000, 10000)
    
    # Set y-axis limits for the bottom subplot (0 to 4000)
    ax_bottom.set_ylim(0, 1000)
    
    # Hide x-axis labels for the top subplot
    ax_top.set_xticklabels([])
    
    # Set labels and adjust layout
    ax_bottom.set_ylabel('Defense Number')
    ax_bottom.set_xticklabels(ax_bottom.get_xticklabels(), rotation=90, ha='center')
    
    # Add legend to the bottom subplot
    ax_bottom.legend(title='Contig Classification', loc='upper right', bbox_to_anchor=(1.15, 1), 
                     frameon=False, fontsize='small')
    
    # Remove x-axis label
    ax_bottom.set_xlabel('')
    
    # Add a break line between the subplots
    d = .015  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False)
    ax_top.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    ax_top.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax_bottom.transAxes)  # switch to the bottom axes
    ax_bottom.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax_bottom.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_file, format='pdf', dpi=300, bbox_inches='tight')
    plt.close(fig)  # Explicitly close the figure

def main():
    parser = argparse.ArgumentParser(description='Create a stacked bar chart showing the frequency of each Defense Type by Contig Classification.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output PDF file')
    args = parser.parse_args()
    
    create_stacked_bar_chart(args.input, args.output)

if __name__ == '__main__':
    main()

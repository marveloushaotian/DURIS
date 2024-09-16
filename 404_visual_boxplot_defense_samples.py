import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def create_boxplot(input_file, output_file, final_result_column, y_axis_label='Defense Number per GB'):
    # Step 1: Load the data
    df = pd.read_csv(input_file)
    
    # Step 2: Create a new column for combined grouping
    df['Group'] = df['Country'] + '_' + df['Location']
    
    # Step 3: Create the boxplot
    fig, axes = plt.subplots(1, 3, figsize=(24, 10))
    
    contig_classifications = sorted(df['Contig_Classification'].unique())
    location_colors = ["#23496d", "#8b68ab", "#8eb19a", "#7396bf"]
    location_color_map = dict(zip(sorted(df['Location'].unique()), location_colors))
    
    for i, cc in enumerate(contig_classifications):
        df_cc = df[df['Contig_Classification'] == cc]
        
        sns.boxplot(x='Country', y=final_result_column, hue='Location', data=df_cc, 
                    ax=axes[i], palette=location_color_map, showfliers=False, width=0.8)
        sns.stripplot(x='Country', y=final_result_column, hue='Location', data=df_cc, 
                      ax=axes[i], palette=location_color_map, dodge=True, alpha=0.5, jitter=True)
        
        axes[i].set_title(f'{cc}', fontsize=14)
        axes[i].set_xlabel('')
        if i == 0:
            axes[i].set_ylabel(y_axis_label, fontsize=14)
        else:
            axes[i].set_ylabel('')
        axes[i].tick_params(axis='x', rotation=0, labelsize=12)
        axes[i].tick_params(axis='y', labelsize=12)
        
        # Remove legend for all subplots
        axes[i].get_legend().remove()
    
    # Add a single legend to the right of the subplots
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles[:len(location_colors)], labels[:len(location_colors)], 
               title='Location', bbox_to_anchor=(1.01, 0.5), loc='center left', 
               fontsize=12, title_fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight', dpi=300)
    plt.close(fig)

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate boxplots for Final Results by Contig Classification, Country, and Location.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input file (CSV format)')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output plot (PDF format)')
    parser.add_argument('-c', '--column', required=True, help='Name of the column representing Final Result')
    parser.add_argument('-y', '--ylabel', default='Defense Number per GB', help='Label for y-axis')
    
    args = parser.parse_args()
    
    # Call the function with provided arguments
    create_boxplot(args.input, args.output, args.column, args.ylabel)

if __name__ == '__main__':
    main()

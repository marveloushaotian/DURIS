import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def create_boxplot(input_file, output_file, defense_num_column):
    # Load the data
    df = pd.read_csv(input_file, sep='\t')

    # Create a new column for combined grouping
    df['Group'] = df['Contig_Group'] + '_' + df['Location_BAF']

    # Create the boxplot with a logarithmic scale
    plt.figure(figsize=(20, 10))
    sns.boxplot(x='Group', y=defense_num_column, data=df, showfliers=False)
    sns.stripplot(x='Group', y=defense_num_column, data=df, color='red', alpha=0.5, jitter=True)

    # Set y-axis to logarithmic scale
    plt.yscale('log')

    # Customize plot
    plt.title(f'Boxplot of {defense_num_column} by Contig Group and Location BAF (Log Scale)')
    plt.xlabel('Contig Group and Location BAF')
    plt.ylabel(f'{defense_num_column} (Log Scale)')
    plt.xticks(rotation=90)
    plt.grid(True, which="both", ls="--")

    # Save and show plot
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='Create a boxplot by Contig Group and Location BAF with logarithmic scale.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
    parser.add_argument('-d', '--defense', type=str, required=True, help='Name of the column representing defense number')
    args = parser.parse_args()

    # Call the function with provided arguments
    create_boxplot(args.input, args.output, args.defense)


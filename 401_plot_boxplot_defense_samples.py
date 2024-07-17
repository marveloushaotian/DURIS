import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_boxplot(input_file, output_file, final_result_column, title):
    # Step 1: Load the data
    logging.info(f"Loading data from {input_file}")
    df = pd.read_csv(input_file, sep='\t')
    
    # Step 2: Create a new column for combined grouping
    logging.info("Creating combined grouping column")
    df['Group'] = df['Contig_Group'] + '_' + df['Location_BAF']
    
    # Step 3: Create the boxplot
    plt.figure(figsize=(20, 10))
    sns.boxplot(x='Group', y=final_result_column, data=df, showfliers=False)
    sns.stripplot(x='Group', y=final_result_column, data=df, color='red', alpha=0.5, jitter=True)
    
    # Step 4: Customize plot
    plt.title(title)
    plt.xlabel('Contig Group and Location BAF')
    plt.ylabel(final_result_column)
    plt.xticks(rotation=90)
    plt.grid(True)
    
    # Step 5: Save and show plot
    plt.tight_layout()
    logging.info(f"Saving plot to {output_file}")
    plt.savefig(output_file, format='pdf')
    plt.show()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate a boxplot for Final Results by Contig Group and Location BAF.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input file (Grouped_Statistics.txt)')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output plot (PDF format)')
    parser.add_argument('-c', '--column', required=True, help='Name of the column representing Final Result')
    parser.add_argument('-t', '--title', default='Boxplot of Final Results by Contig Group and Location BAF', help='Title of the plot')
    
    args = parser.parse_args()
    
    # Call the function with provided arguments
    create_boxplot(args.input, args.output, args.column, args.title)

if __name__ == '__main__':
    main()


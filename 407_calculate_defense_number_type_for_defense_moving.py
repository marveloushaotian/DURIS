import pandas as pd
import argparse
import os
from tqdm import tqdm

def process_file(input_file, output_file):
    # Load the file into a DataFrame
    df = pd.read_csv(input_file)

    # Filter for specific Defense Types
    selected_defense_types = ['PD_T4_6', 'RM', 'SoFic', 'CRISPRCas', 'AbiE', 'CBASS', 'Septu', 'Wadjet', 'AbiD', 'Zorya']
    df = df[df['Defense_Type'].isin(selected_defense_types)]

    # Get unique Defense_Type values
    all_defense_types = df['Defense_Type'].unique()

    # Initialize the combined DataFrame with Defense_Type as the index
    combined_df = pd.DataFrame(index=all_defense_types)

    # Handle Phage counts
    phage_df = df[df['Contig_Classification'] == 'Phage']
    phage_counts = phage_df['Defense_Type'].value_counts()
    combined_df['Phage'] = combined_df.index.map(phage_counts).fillna(0)

    # Handle Plasmid counts
    plasmid_df = df[df['Contig_Classification'] == 'Plasmid']
    plasmid_counts = plasmid_df['Defense_Type'].value_counts()
    combined_df['Plasmid'] = combined_df.index.map(plasmid_counts).fillna(0)

    # Handle Chromosome with classification by Kaiju_Phylum
    chromosome_df = df[df['Contig_Classification'] == 'Chromosome']
    
    # Filter for specific Kaiju_Phylum
    selected_phyla = ['Pseudomonadota', 'Bacteroidota', 'Bacillota', 'Campylobacterota', 
                      'Actinomycetota', 'Myxococcota', 'Verrucomicrobiota', 'Thermodesulfobacteriota']
    chromosome_df = chromosome_df[chromosome_df['Kaiju_Phylum'].isin(selected_phyla)]

    grouped = chromosome_df.groupby(['Defense_Type', 'Kaiju_Phylum']).size().reset_index(name='Counts')
    pivot_table = grouped.pivot(index='Defense_Type', columns='Kaiju_Phylum', values='Counts').fillna(0)

    # Add these as columns to the combined DataFrame
    for phylum in selected_phyla:
        if phylum in pivot_table.columns:
            combined_df[phylum] = combined_df.index.map(pivot_table[phylum]).fillna(0)
        else:
            combined_df[phylum] = 0

    # Reorder columns
    column_order = selected_phyla + ['Plasmid', 'Phage']
    combined_df = combined_df[column_order]

    # Rename the columns
    column_map = {
        'Pseudomonadota': 'Ps', 'Bacteroidota': 'Ba', 'Bacillota': 'Bc', 'Campylobacterota': 'Ca',
        'Actinomycetota': 'Ac', 'Myxococcota': 'My', 'Verrucomicrobiota': 'Ve', 'Thermodesulfobacteriota': 'Th',
        'Plasmid': 'Pm', 'Phage': 'Ph'
    }
    combined_df.columns = combined_df.columns.map(lambda x: column_map.get(x, x))

    # Reorder rows
    row_order = ['PD_T4_6', 'RM', 'SoFic', 'CRISPRCas', 'AbiE', 'CBASS', 'Septu', 'Wadjet', 'AbiD', 'Zorya']
    combined_df = combined_df.reindex(row_order)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_file)

    print(f"Processing complete. Results saved to {output_file}")

def process_directory(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all CSV files in the input directory
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    # Process each file with a progress bar
    for input_file in tqdm(csv_files, desc="Processing files"):
        input_path = os.path.join(input_dir, input_file)
        output_file = os.path.join(output_dir, f"processed_{input_file}")
        process_file(input_path, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process contig classification data into combined tables.")
    parser.add_argument('-i', '--input_dir', required=True, help="Input directory containing CSV files")
    parser.add_argument('-o', '--output_dir', required=True, help="Output directory for processed CSV files")

    args = parser.parse_args()

    process_directory(args.input_dir, args.output_dir)

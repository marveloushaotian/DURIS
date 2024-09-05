import pandas as pd
import argparse

def process_file(input_file, output_file):
    # Load the file into a DataFrame
    df = pd.read_csv(input_file, sep='\t')

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

    # Save the combined DataFrame to a text file
    combined_df.to_csv(output_file, sep='\t')

    print(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process contig classification data into a single combined table.")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output file path")

    args = parser.parse_args()

    process_file(args.input, args.output)

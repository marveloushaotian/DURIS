import pandas as pd
import os
import argparse
from tqdm import tqdm

def process_csv(input_file, output_dir):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Filter Defense_Type and Contig_Classification
    # defense_types = ['SoFic', 'PD_T4_6', 'RM', 'CRISPRCas', 'AbiE', 'CBASS', 'DRT', 'AbiL', 'Septu', 'AbiD', 'Wadjet', 'Mokosh', 'Gabija', 'Zorya', 'ietAS', 'Thoeris', 'Uzume', 'SEFIR', 'darTG']
    defense_types = ['SoFic', 'PD_T4_6', 'RM', 'CRISPRCas', 'AbiE', 'CBASS', 'DRT', 'AbiL', 'Septu', 'AbiD']
    contig_classifications = ['Pseudomonadota', 'Bacteroidota', 'Bacillota', 'Campylobacterota', 
                              'Actinomycetota', 'Myxococcota', 'Verrucomicrobiota', 'Thermodesulfobacteriota', 
                              'Plasmid', 'Phage']
    
    df = df[df['Defense_Type'].isin(defense_types) & df['Contig_Classification'].isin(contig_classifications)]
    
    # Group by Location and Country
    grouped = df.groupby(['Location', 'Country'])
    
    # Define column name mapping
    column_mapping = {
        'Pseudomonadota': 'Ps', 'Bacteroidota': 'Ba', 'Bacillota': 'Bc', 'Campylobacterota': 'Ca',
        'Actinomycetota': 'Ac', 'Myxococcota': 'My', 'Verrucomicrobiota': 'Ve', 'Thermodesulfobacteriota': 'Th',
        'Plasmid': 'Pm', 'Phage': 'Ph'
    }
    
    # Iterate through each group with progress bar
    for (location, country), group_data in tqdm(grouped, desc="Processing groups"):
        # Create a pivot table
        pivot_table = pd.pivot_table(group_data, 
                                     values='GCGB', 
                                     index='Defense_Type', 
                                     columns='Contig_Classification', 
                                     fill_value=0)
        
        # Ensure all defense types and contig classifications are present
        for dt in defense_types:
            if dt not in pivot_table.index:
                pivot_table.loc[dt] = 0
        for cc in contig_classifications:
            if cc not in pivot_table.columns:
                pivot_table[cc] = 0
        
        # Reorder columns and rows
        pivot_table = pivot_table.reindex(columns=contig_classifications, index=defense_types)
        
        # Rename columns
        pivot_table.rename(columns=column_mapping, inplace=True)
        
        # Create output filename
        output_filename = f"{location}_{country}.csv"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save the pivot table to CSV
        pivot_table.to_csv(output_path)
        print(f"Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Process Circular_GCGB_selected.csv into grouped files.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output directory for grouped files')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Process the CSV file
    process_csv(args.input, args.output)

if __name__ == "__main__":
    main()

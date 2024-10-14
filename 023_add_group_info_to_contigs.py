import pandas as pd
import argparse
from tqdm import tqdm

# Load the actual group data from the file
group_file_path = 'Collect/00_Metadata/Sample_Group.csv'
group_data = pd.read_csv(group_file_path)

def process_contig_id(input_file_path, output_file_path, contig_id_column='Contig_ID', sample_name_column='Sample_Name'):
    # Load the data
    data = pd.read_csv(input_file_path)

    # Function to extract sample name
    def extract_sample_name(contig_id):
        if contig_id.startswith('18097D'):
            parts = contig_id.split('-')
            if len(parts) >= 3:
                number_part = ''.join(filter(str.isdigit, parts[2]))
                return f'Sample_{int(number_part):02d}'
        elif contig_id.startswith('DP'):
            parts = contig_id.split('-')
            if len(parts) >= 2:
                number_part = ''.join(filter(str.isdigit, parts[1]))
                return f'Sample_{int(number_part):02d}'
        return None

    # Apply the function to create the Sample_Name column
    tqdm.pandas(desc="Extracting sample names")
    data[sample_name_column] = data[contig_id_column].progress_apply(extract_sample_name)

    # Merge with the sample group data from the group file
    merged_data = pd.merge(data, group_data, left_on=sample_name_column, right_on='Sample', how='left')

    # Ensure all original columns are preserved
    for col in data.columns:
        if col not in merged_data.columns:
            merged_data[col] = data[col]

    # Save the processed data
    merged_data.to_csv(output_file_path, index=False)

    print(f"Processed data saved to {output_file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Contig_ID to generate Sample_Name and enrich with sample group info')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Path to save the processed CSV file')
    parser.add_argument('--contig_id_column', type=str, default='Contig_ID', help='Name of the column containing Contig_ID')
    parser.add_argument('--sample_name_column', type=str, default='Sample', help='Name of the new column to create for sample names')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, 
                        help='Show this help message and exit')

    args = parser.parse_args()

    process_contig_id(args.input_file, args.output_file, args.contig_id_column, args.sample_name_column)

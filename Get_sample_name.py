import pandas as pd
import argparse

def process_contig_id(input_file_path, output_file_path, contig_id_column='Contig_ID', sample_name_column='Sample_Name'):
    # Load the data
    data = pd.read_csv(input_file_path, sep='\t')

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
    data[sample_name_column] = data[contig_id_column].apply(extract_sample_name)

    # Save the processed data
    data.to_csv(output_file_path, sep='\t', index=False)

    print(f"Processed data saved to {output_file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Contig_ID to generate Sample_Name')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input file')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save the processed file')
    parser.add_argument('--contig_id_column', type=str, default='Contig_ID', help='Name of the column containing Contig_ID')
    parser.add_argument('--sample_name_column', type=str, default='Sample_Name', help='Name of the new column to create for sample names')

    args = parser.parse_args()

    process_contig_id(args.input_file, args.output_file, args.contig_id_column, args.sample_name_column)


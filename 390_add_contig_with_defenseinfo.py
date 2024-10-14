import argparse
import logging
from tqdm import tqdm

# Setup logging
logging.basicConfig(filename='add_defense_type_column_to_abundance_profile.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def parse_defense_info(file_path):
    """
    Parses the defense mechanism file to create a mapping of sequence identifiers to defense mechanisms.
    """
    mapping = {}
    with open(file_path, 'r') as f:
        for line in tqdm(f, desc="Parsing defense info"):
            if line.startswith('>'):
                parts = line.split(';')
                node_id = parts[0].split()[0][1:]  # Remove '>' and split by space, then take the first part
                defense_mechanism = parts[-1].split('=')[-1].strip()
                mapping[node_id] = defense_mechanism
    return mapping

def add_defense_column_to_abundance_profile(defense_info_path, abundance_profile_path, output_path):
    """
    Adds a new column for the defense mechanism to the abundance profile.
    """
    # Parse defense info to get the mapping
    mapping = parse_defense_info(defense_info_path)

    with open(abundance_profile_path, 'r') as infile, open(output_path, 'w') as outfile:
        header = next(infile).strip().split('\t')
        outfile.write('DefenseType\t' + '\t'.join(header) + '\n')  # Add 'DefenseType' as the new first column name

        for line in tqdm(infile, desc="Updating abundance profile"):
            parts = line.strip().split('\t')
            node_id = parts[0]
            defense_type = mapping.get(node_id, 'Unknown')  # Use 'Unknown' if the defense type is not in the mapping
            outfile.write(defense_type + '\t' + '\t'.join(parts) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add defense mechanism as a new column in the abundance profile.')
    parser.add_argument('-i', '--input_defense_info', required=True, help='Input file with defense mechanism information.')
    parser.add_argument('-a', '--input_abundance_profile', required=True, help='Input file with abundance profile.')
    parser.add_argument('-o', '--output', required=True, help='Output file path for the updated abundance profile with the defense mechanism column added.')
    args = parser.parse_args()

    logging.info('Script started.')
    add_defense_column_to_abundance_profile(args.input_defense_info, args.input_abundance_profile, args.output)
    logging.info('Script finished.')


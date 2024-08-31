import argparse
from tqdm import tqdm

def parse_defense_info(file_path):
    """
    Parses the defense mechanism file and returns a mapping of sequence identifiers to defense mechanisms.
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

def update_abundance_profile(defense_info_path, abundance_profile_path, output_path):
    """
    Updates the abundance profile with defense mechanisms based on the provided mapping.
    """
    # Parse defense info to get the mapping
    mapping = parse_defense_info(defense_info_path)

    with open(abundance_profile_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in tqdm(infile, desc="Updating abundance profile"):
            parts = line.strip().split('\t')
            node_id = parts[0]
            if node_id in mapping:
                parts[0] = mapping[node_id]  # Replace the ID with its defense mechanism
            outfile.write('\t'.join(parts) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update abundance profile with defense mechanisms.')
    parser.add_argument('-i', '--input_defense_info', required=True, help='Input file with defense mechanism information.')
    parser.add_argument('-a', '--input_abundance_profile', required=True, help='Input file with abundance profile.')
    parser.add_argument('-o', '--output', required=True, help='Output file path for the updated abundance profile.')

    args = parser.parse_args()

    print('Script started.')
    update_abundance_profile(args.input_defense_info, args.input_abundance_profile, args.output)
    print('Script finished.')

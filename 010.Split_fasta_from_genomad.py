import argparse
from tqdm import tqdm

def read_ids_from_tsv(tsv_file):
    with open(tsv_file, 'r') as file:
        ids = [line.split('\t')[0].strip() for line in file.readlines()]
    return set(ids)

def split_fasta_by_ids(fasta_file, ids, output1, output2):
    with open(fasta_file, 'r') as file:
        lines = file.readlines()
    
    matching_lines = []
    non_matching_lines = []
    current_sequence = []
    in_matching_sequence = False

    for line in tqdm(lines, desc="Processing FASTA file"):
        if line.startswith('>'):
            if current_sequence:
                if in_matching_sequence:
                    matching_lines.extend(current_sequence)
                else:
                    non_matching_lines.extend(current_sequence)
            current_sequence = [line]
            seq_id = line.split()[0][1:]
            in_matching_sequence = seq_id in ids
        else:
            current_sequence.append(line)
    
    if current_sequence:
        if in_matching_sequence:
            matching_lines.extend(current_sequence)
        else:
            non_matching_lines.extend(current_sequence)

    with open(output1, 'w') as file:
        file.writelines(matching_lines)
    
    with open(output2, 'w') as file:
        file.writelines(non_matching_lines)

def main(args):
    ids = read_ids_from_tsv(args.tsv)
    split_fasta_by_ids(args.fasta, ids, args.output1, args.output2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split FASTA sequences based on TSV IDs.')
    parser.add_argument('-t', '--tsv', required=True, help='Path to the TSV file containing sequence IDs.')
    parser.add_argument('-f', '--fasta', required=True, help='Path to the FASTA file.')
    parser.add_argument('-o1', '--output1', required=True, help='Output file for matching sequences.')
    parser.add_argument('-o2', '--output2', required=True, help='Output file for non-matching sequences.')
    args = parser.parse_args()
    main(args)


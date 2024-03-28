import argparse
import glob
from tqdm import tqdm

def read_gff(file_path):
    """Read GFF file and return a dictionary mapping sequence names to types."""
    seq_type_dict = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) > 2:
                seq_name = parts[0]
                seq_type = parts[2]
                seq_type_dict[seq_name] = seq_type
    return seq_type_dict

def process_fasta(fasta_file_path, seq_type_dict, output_file_path):
    """Process FASTA file, keeping only matching sequences and appending types to sequence names."""
    with open(fasta_file_path, 'r') as fasta_file:
        lines = fasta_file.readlines()
        processed_lines = []
        for i in tqdm(range(0, len(lines), 2), desc=f"Processing {fasta_file_path}"):
            line = lines[i]
            if line.startswith('>'):
                seq_name = line[1:].strip().split(' ')[0]
                if seq_name in seq_type_dict:
                    line = line.strip() + ';' + seq_type_dict[seq_name] + '\n'
                    processed_lines.append(line)
                    processed_lines.append(lines[i+1])
    with open(output_file_path, 'a') as output_file:
        output_file.writelines(processed_lines)

def main():
    parser = argparse.ArgumentParser(description="Filter and annotate FASTA sequences based on GFF annotations.")
    parser.add_argument("-i", "--input_fasta", required=True, help="Input FASTA file path or wildcard pattern")
    parser.add_argument("-g", "--gff", required=True, help="GFF file path for annotations")
    parser.add_argument("-o", "--output_fasta", required=True, help="Output FASTA file path where results are appended")

    args = parser.parse_args()

    # Read GFF file once and use for all FASTA files
    seq_type_dict = read_gff(args.gff)

    # Process each FASTA file matched by the wildcard pattern
    for fasta_file_path in glob.glob(args.input_fasta):
        process_fasta(fasta_file_path, seq_type_dict, args.output_fasta)
    print(f"All sequences processed and appended to {args.output_fasta}")

if __name__ == "__main__":
    main()


import argparse
from tqdm import tqdm

def read_gff(file_path):
    """Reads a GFF file and returns a mapping of sequence names to their types."""
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
    """Processes a FASTA file to only retain sequences that match the GFF annotations, appending the type to the sequence name line, and including all lines up to the next sequence header."""
    with open(fasta_file_path, 'r') as fasta_file, open(output_file_path, 'w') as output_file:
        write_mode = False
        for line in tqdm(fasta_file, desc="Processing"):
            if line.startswith('>'):
                seq_name = line[1:].strip().split(' ')[0]
                if seq_name in seq_type_dict:
                    line = line.strip() + ';' + seq_type_dict[seq_name] + '\n'
                    output_file.write(line)
                    write_mode = True
                else:
                    write_mode = False
            elif write_mode:
                output_file.write(line)

    print(f"Processed sequences saved to {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Filter and annotate FASTA sequences based on GFF annotations.",
                                     epilog="Example usage: python script_name.py --input_fasta path/to/your/input.fasta --gff path/to/your/annotations.gff --output_fasta path/to/your/output.fasta")
    parser.add_argument("-i", "--input_fasta", required=True, help="Input FASTA file path")
    parser.add_argument("-g", "--gff", required=True, help="GFF file path for annotations")
    parser.add_argument("-o", "--output_fasta", required=True, help="Output FASTA file path")

    args = parser.parse_args()

    seq_type_dict = read_gff(args.gff)
    process_fasta(args.input_fasta, seq_type_dict, args.output_fasta)

if __name__ == "__main__":
    main()


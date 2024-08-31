import argparse
from math import ceil

def split_fasta(fasta_file, num_files):
    """
    Split a FASTA file into a specified number of smaller files.

    Parameters:
    fasta_file (str): Path to the input FASTA file.
    num_files (int): Number of smaller FASTA files to create.
    """
    # Read the original FASTA file
    with open(fasta_file, 'r') as file:
        sequences = file.read().split('>')[1:]  # Split sequences and remove the first empty string

    # Calculate the number of sequences per file
    sequences_per_file = ceil(len(sequences) / num_files)

    for i in range(num_files):
        output_file_name = f"{fasta_file.rsplit('.', 1)[0]}_{i+1}.fasta"
        with open(output_file_name, 'w') as output_file:
            for sequence in sequences[i * sequences_per_file : (i + 1) * sequences_per_file]:
                output_file.write(f">{sequence}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a FASTA file into a specified number of smaller files.',
                                     epilog='Example: %(prog)s -i input.fasta -n 3')
    parser.add_argument('-i', type=str, required=True, help='Path to the input FASTA file')
    parser.add_argument('-n', type=int, required=True, help='Number of smaller FASTA files to create')
    args = parser.parse_args()

    split_fasta(args.i, args.n)

    print(f"Successfully split {args.i} into {args.n} files.")

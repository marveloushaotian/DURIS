import sys
from math import ceil

def split_fasta(fasta_file, num_files):
    """
    Split a FASTA file into a specified number of smaller FASTA files.

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
    if len(sys.argv) != 3:
        print("Usage: python split_fasta.py <fasta_file> <num_files>")
        sys.exit(1)

    fasta_file = sys.argv[1]
    num_files = int(sys.argv[2])

    split_fasta(fasta_file, num_files)


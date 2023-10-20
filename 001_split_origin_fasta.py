import os
import argparse
from tqdm import tqdm

def split_fasta(input_file, output_dir, chunk_size=1000):
    """
    1. Ensure output directory exists
    2. Initialize variables
    3. Open and read the fasta file
    4. Write to a new file if buffer reaches chunk size
    5. Write remaining lines to a new file
    """
    # Step 1: Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Step 2: Initialize variables
    count = 0
    file_count = 1
    buffer = []

    # Step 3: Open and read the fasta file
    with open(input_file, 'r') as f:
        for line in tqdm(f, desc="Reading lines"):
            # Add line to buffer
            buffer.append(line)

            # Check if this is a new entry (starts with '>')
            if line.startswith('>'):
                count += 1

            # Step 4: Write to a new file if buffer reaches chunk size
            if count > chunk_size:
                output_file = os.path.join(output_dir, f'split_{file_count}.fasta')
                with open(output_file, 'w') as out_f:
                    out_f.writelines(buffer[:-1])  # Exclude the last '>'

                # Reset variables
                buffer = [buffer[-1]]  # Start the next chunk with the last '>'
                count = 1  # Reset the count for the next chunk
                file_count += 1

    # Step 5: Write remaining lines to a new file
    if buffer:
        output_file = os.path.join(output_dir, f'split_{file_count}.fasta')
        with open(output_file, 'w') as out_f:
            out_f.writelines(buffer)

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Split a FASTA file into smaller chunks.')
    parser.add_argument('-i', type=str, help='Path to the input FASTA file.')
    parser.add_argument('-o', type=str, help='Path to the output directory.')
    parser.add_argument('-s', type=int, default=1000, help='Number of sequences per chunk.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the function
    split_fasta(args.input_file, args.output_dir, args.chunk_size)


import os
import argparse
from tqdm import tqdm

def split_fasta(input_file, output_dir, chunk_size=1000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = 0
    file_count = 1
    buffer = []

    with open(input_file, 'r') as f:
        for line in tqdm(f, desc="Reading lines"):
            buffer.append(line)

            if line.startswith('>'):
                count += 1

            if count > chunk_size:
                output_file = os.path.join(output_dir, f'split_{file_count}.fasta')
                with open(output_file, 'w') as out_f:
                    out_f.writelines(buffer[:-1])

                buffer = [buffer[-1]]
                count = 1
                file_count += 1

    if buffer:
        output_file = os.path.join(output_dir, f'split_{file_count}.fasta')
        with open(output_file, 'w') as out_f:
            out_f.writelines(buffer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a FASTA file into smaller chunks based on the number of sequences.',
                                     epilog="Example usage: python script_name.py -i path/to/your/input.fasta -o path/to/output/directory -s 500\nReplace 'script_name.py' with this script's filename, and specify the paths and chunk size as needed.")
    parser.add_argument('-i', dest='input_file', type=str, required=True, help='Path to the input FASTA file.')
    parser.add_argument('-o', dest='output_dir', type=str, required=True, help='Path to the output directory.')
    parser.add_argument('-s', dest='chunk_size', type=int, default=1000, help='Number of sequences per chunk.')

    args = parser.parse_args()

    split_fasta(args.input_file, args.output_dir, args.chunk_size)


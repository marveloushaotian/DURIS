import argparse
import glob
import os
import subprocess
import json
from tqdm import tqdm

def run_mmseqs(input_file, output_dir, min_seq_id, coverage, cov_mode):
    """
    Run the mmseqs command in the specified output folder and generate the output.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(output_dir))  # Prefix with the folder name
    tmp_dir = os.path.join(output_dir, 'tmp')  # Create a tmp subfolder for each output folder
    log_err = os.path.join(output_dir, 'log.err')
    log_out = os.path.join(output_dir, 'log.out')
    command = f"mmseqs easy-cluster {input_file} {output_file} {tmp_dir} " \
              f"--min-seq-id {min_seq_id} -c {coverage} --cov-mode {cov_mode} " \
              f"2>{log_err} >{log_out}"
    subprocess.run(command, shell=True, check=True)

def main(input_prefix, output_folder, min_seq_id, coverage, cov_mode):
    """
    Process all files in the input folder with the given prefix and create new folders in the output folder for each file.
    """
    input_files = glob.glob(f"{input_prefix}*.fasta")

    for input_file in tqdm(input_files, desc="Processing files"):
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(output_folder, file_name)
        run_mmseqs(input_file, output_dir, min_seq_id, coverage, cov_mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process plasmid files with mmseqs and output the results in separate folders.')
    parser.add_argument('-i', '--input', help='Input file prefix', required=True)
    parser.add_argument('-o', '--output', help='Output folder', required=True)
    parser.add_argument('--min_seq_id', help='Minimum sequence identity for mmseqs', type=float, default=0.9)
    parser.add_argument('--coverage', help='Coverage for mmseqs', type=float, default=0.95)
    parser.add_argument('--cov_mode', help='Coverage mode for mmseqs', type=int, default=0)

    args = parser.parse_args()

    main(args.input, args.output, args.min_seq_id, args.coverage, args.cov_mode)


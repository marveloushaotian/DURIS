import os
import subprocess
import sys
import argparse
from pathlib import Path
from tqdm import tqdm

def run_mmseqs(input_file, output_dir, min_seq_id, coverage, cov_mode):
    """
    Executes the mmseqs easy-cluster command with specified parameters.
    
    Parameters:
    - input_file: Path to the input FASTA file.
    - output_dir: Directory to store the output and logs.
    - min_seq_id: Minimum sequence identity for clustering.
    - coverage: Coverage for mmseqs.
    - cov_mode: Coverage mode for mmseqs.
    """
    # Create output, temporary, and log directories
    output_path = Path(output_dir)
    tmp_dir = output_path / "tmp"
    log_dir = output_path / "log"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(exist_ok=True)

    # Define file prefix and command
    prefix = input_file.stem
    cmd = (
        f"mmseqs easy-cluster {input_file} {output_path}/{prefix} {tmp_dir} "
        f"--min-seq-id {min_seq_id} -c {coverage} --cov-mode {cov_mode} "
        f"2>{log_dir}/log.err >{log_dir}/log.out; touch {output_path}/{prefix}_all_seqs.fasta"
    )

    # Execute the command
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing MMseqs2 for {input_file}: {e}", file=sys.stderr)

def main():
    """
    Processes all FASTA files in the specified input directory with MMseqs2.
    """
    parser = argparse.ArgumentParser(
        description='Run mmseqs on multiple FASTA files.',
        epilog='Example: python script.py -i ./input_dir -o ./output_dir --min_seq_id 0.9 --coverage 0.95 --cov_mode 0'
    )
    parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory containing .fasta files')
    parser.add_argument('-o', '--output_dir', type=str, required=True, help='Output directory to store results')
    parser.add_argument('--min_seq_id', type=float, default=0.9, help='Minimum sequence identity for mmseqs')
    parser.add_argument('--coverage', type=float, default=0.95, help='Coverage for mmseqs')
    parser.add_argument('--cov_mode', type=int, default=0, help='Coverage mode for mmseqs')
    
    args = parser.parse_args()

    # Process each FASTA file in the input directory
    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)
    fasta_files = list(input_path.glob('*.fasta'))
    
    if not fasta_files:
        print(f"No FASTA files found in {input_path}.", file=sys.stderr)
        sys.exit(1)

    for fasta_file in tqdm(fasta_files, desc="Processing files"):
        output_folder = output_path / fasta_file.stem
        run_mmseqs(fasta_file, output_folder, args.min_seq_id, args.coverage, args.cov_mode)

if __name__ == "__main__":
    main()


import argparse
import subprocess
import os
from tqdm import tqdm
import glob
import logging

# Setting up argument parser
parser = argparse.ArgumentParser(description="""Batch BWA MEM script.
Example usage: python batch_bwa_mem.py -i /path/to/fastq_dir -p prefix -o /path/to/output_dir --log bwa_mem.log""",
formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--input', help='Input directory containing fastq.gz files. Example: -i /path/to/fastq', required=True)
parser.add_argument('-p', '--prefix', help='Prefix for rep_seq.fasta. Example: -p prefix', required=True)
parser.add_argument('-o', '--output', help='Output directory. Example: -o /path/to/output', required=True)
parser.add_argument('--log', help='Log file name. Example: --log bwa_mem.log', default='bwa_mem.log')
parser.add_argument('-t', '--threads', help='Number of threads. Example: -t 8', default='8', type=str)

args = parser.parse_args()

# Setting up logging
logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s - %(message)s')

# Ensure output directory exists
bwa_output_dir = os.path.join(args.output, 'bwa')
os.makedirs(bwa_output_dir, exist_ok=True)

# Function to find fastq.gz file pairs
def find_fastq_pairs(directory):
    fastq_files = glob.glob(os.path.join(directory, "*_qc_[12].fastq.gz"))
    paired_files = {}
    for file in fastq_files:
        base_name = os.path.basename(file).rsplit("_", 2)[0]
        if base_name in paired_files:
            paired_files[base_name].append(file)
        else:
            paired_files[base_name] = [file]
    return [tuple(sorted(pairs)) for pairs in paired_files.values() if len(pairs) == 2]

# Function to run bwa mem command
def run_bwa_mem(prefix, fastq1, fastq2, output_dir, threads):
    fasta_file = f"{prefix}_rep_seq.fasta"
    output_file = os.path.join(output_dir, os.path.basename(fastq1).replace('_qc_1.fastq.gz', '.sam'))
    cmd = ['bwa', 'mem', '-M', '-t', threads, fasta_file, fastq1, fastq2, '>', output_file]
    try:
        subprocess.run(' '.join(cmd), shell=True, check=True)
        logging.info(f"Successfully processed {fastq1} and {fastq2}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {fastq1} and {fastq2}: {e}")

# Main script execution
if __name__ == '__main__':
    fastq_pairs = find_fastq_pairs(args.input)
    for fastq1, fastq2 in tqdm(fastq_pairs, desc="Processing fastq file pairs"):
        run_bwa_mem(args.prefix, fastq1, fastq2, bwa_output_dir, args.threads)


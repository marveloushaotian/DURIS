import argparse
import subprocess
import logging
from tqdm import tqdm

# Setting up argument parser
parser = argparse.ArgumentParser(description='Script to run bwa index with given prefix(es). \
Example usage: python bwa_index_script.py -i prefix1 -o some_output_directory --log my_log.log',
formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--input', nargs='+', help='Input prefix(es) for fasta files. Example: -i prefix1 prefix2', required=True)
parser.add_argument('-o', '--output', help='Output directory (not used in this script, included for consistency). Example: -o output_directory', required=False)
parser.add_argument('--log', help='Log file name. Example: --log my_log.log', default='bwa_index.log')

args = parser.parse_args()

# Setting up logging
logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to run bwa index command
def run_bwa_index(prefix):
    fasta_file = f"{prefix}_rep_seq.fasta"
    cmd = ['bwa', 'index', fasta_file]
    try:
        subprocess.check_call(cmd)
        logging.info(f"Successfully indexed {fasta_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in indexing {fasta_file}: {e}")

# Main script execution
if __name__ == '__main__':
    for prefix in tqdm(args.input, desc="Indexing fasta files"):
        run_bwa_index(prefix)


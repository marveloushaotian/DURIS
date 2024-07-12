import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import logging
import time
import os

# Setup logging with unique filename
log_filename = f'bam_filtering_{time.strftime("%Y%m%d_%H%M%S")}_{os.getpid()}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def filter_bam_files(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sorted_bam_files = list(input_dir.glob('*_sort.bam'))
    for bam_file in tqdm(sorted_bam_files, desc='Filtering BAM files'):
        output_file = output_dir / (bam_file.stem + '_filter.bam')
        cmd = ['msamtools', 'filter', '-b', '-l', '80', '-p', '90', '-z', '80', '--besthit', str(bam_file), '>', str(output_file)]
        cmd_string = " ".join(cmd)
        subprocess.run(cmd_string, shell=True, check=True)
        logging.info(f'Filtered {bam_file} to {output_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter sorted BAM files using msamtools.',
                                     epilog='Example: python script.py -i /path/to/sorted_bam_files -o /path/to/filtered_bam_files')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing sorted BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for filtered BAM files')
    args = parser.parse_args()

    try:
        filter_bam_files(args.input, args.output)
        logging.info("Filtering completed successfully.")
    except Exception as e:
        logging.error(f"Error during filtering: {e}")


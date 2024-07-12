import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import logging
import time
import os

# Setup logging with unique filename
log_filename = f'bam_sorting_{time.strftime("%Y%m%d_%H%M%S")}_{os.getpid()}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def sort_bam_files(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bam_files = list(input_dir.glob('*.bam'))
    for bam_file in tqdm(bam_files, desc='Sorting BAM files'):
        output_file = output_dir / (bam_file.stem + '_sort.bam')
        subprocess.run(['samtools', 'sort', '-n', '-@', '8', bam_file, '-o', output_file], check=True)
        logging.info(f'Sorted {bam_file} to {output_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort BAM files using samtools.',
                                     epilog='Example: python script.py -i /path/to/bam_files -o /path/to/sorted_bam_files')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for sorted BAM files')
    args = parser.parse_args()

    try:
        sort_bam_files(args.input, args.output)
        logging.info("Sorting completed successfully.")
    except Exception as e:
        logging.error(f"Error during sorting: {e}")


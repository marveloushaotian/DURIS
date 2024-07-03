import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import logging
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging with unique filename
log_filename = f'bam_sorting_{time.strftime("%Y%m%d_%H%M%S")}_{os.getpid()}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def sort_bam_file(bam_file, output_dir):
    output_file = output_dir / (bam_file.stem + '_sort.bam')
    try:
        subprocess.run(['samtools', 'sort', '-n', '-@', '8', bam_file, '-o', output_file], check=True)
        logging.info(f'Sorted {bam_file} to {output_file}')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error sorting {bam_file}: {e}")

def main(input_dir, output_dir, num_workers):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bam_files = list(input_dir.glob('*.bam'))
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(sort_bam_file, bam_file, output_dir): bam_file for bam_file in bam_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Sorting BAM files'):
            bam_file = futures[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing {bam_file}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort BAM files using samtools.',
                                     epilog='Example: python script.py -i /path/to/bam_files -o /path/to/sorted_bam_files -w 4')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for sorted BAM files')
    parser.add_argument('-w', '--workers', type=int, default=4, help='Number of parallel workers')
    args = parser.parse_args()

    try:
        main(args.input, args.output, args.workers)
        logging.info("Sorting completed successfully.")
    except Exception as e:
        logging.error(f"Error during sorting: {e}")


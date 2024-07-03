import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import logging
import time
import os

# Setup logging with unique filename
log_filename = f'msamtools_profile_{time.strftime("%Y%m%d_%H%M%S")}_{os.getpid()}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def profile_bam_files(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filter_bam_files = list(input_dir.glob('*_sort_filter.bam'))
    for bam_file in tqdm(filter_bam_files, desc='Generating profiles from BAM files'):
        output_file = output_dir / (bam_file.stem + '_profile_rb.txt')
        cmd = ['msamtools', 'profile', '--multi=all', '--unit=fpkm', '--label=' + bam_file.name, '-o', str(output_file), str(bam_file)]
        subprocess.run(cmd, check=True)
        logging.info(f'Generated profile for {bam_file} into {output_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate profiles from filtered BAM files using msamtools.',
                                     epilog='Example: python script.py -i /path/to/filtered_bam_files -o /path/to/profile_output')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing filtered BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for profile text files')
    args = parser.parse_args()

    try:
        profile_bam_files(args.input, args.output)
        logging.info("Profile generation completed successfully.")
    except Exception as e:
        logging.error(f"Error during profile generation: {e}")


import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def filter_bam_file(bam_file, output_dir):
    output_file = output_dir / (bam_file.stem + '_filter.bam')
    cmd = ['msamtools', 'filter', '-b', '-l', '80', '-p', '90', '-z', '80', '--besthit', str(bam_file), '>', str(output_file)]
    cmd_string = " ".join(cmd)
    try:
        subprocess.run(cmd_string, shell=True, check=True)
        print(f'Filtered {bam_file} to {output_file}')
    except subprocess.CalledProcessError as e:
        print(f"Error filtering {bam_file}: {e}")

def main(input_dir, output_dir, num_workers):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sorted_bam_files = list(input_dir.glob('*_sort.bam'))
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(filter_bam_file, bam_file, output_dir): bam_file for bam_file in sorted_bam_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Filtering BAM files'):
            bam_file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {bam_file}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter sorted BAM files using msamtools.',
                                     epilog='Example: python script.py -i /path/to/sorted_bam_files -o /path/to/filtered_bam_files -w 4')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing sorted BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for filtered BAM files')
    parser.add_argument('-w', '--workers', type=int, default=4, help='Number of parallel workers')
    args = parser.parse_args()

    try:
        main(args.input, args.output, args.workers)
        print("Filtering completed successfully.")
    except Exception as e:
        print(f"Error during filtering: {e}")

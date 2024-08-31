import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_sam_to_bam(sam_file, output_dir):
    output_file = output_dir / sam_file.with_suffix('.bam').name
    try:
        subprocess.run(['samtools', 'view', '-Sb', sam_file, '-o', output_file], check=True)
        print(f'Converted {sam_file} to {output_file}')
    except subprocess.CalledProcessError as e:
        print(f"Error converting {sam_file} to BAM: {e}")

def main(input_dir, output_dir, num_workers):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sam_files = list(input_dir.glob('*.sam'))
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(convert_sam_to_bam, sam_file, output_dir): sam_file for sam_file in sam_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Converting SAM to BAM'):
            sam_file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {sam_file}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert SAM files to BAM format using samtools.',
                                     epilog='Example: python script.py -i /path/to/sam_files -o /path/to/bam_files -w 4')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing SAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for BAM files')
    parser.add_argument('-w', '--workers', type=int, default=4, help='Number of parallel workers')
    args = parser.parse_args()

    try:
        main(args.input, args.output, args.workers)
        print("Conversion completed successfully.")
    except Exception as e:
        print(f"Error during conversion: {e}")

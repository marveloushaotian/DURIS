import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import logging

# Setup logging
logging.basicConfig(filename='sam_to_bam_conversion.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def convert_sam_to_bam(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sam_files = list(input_dir.glob('*.sam'))
    for sam_file in tqdm(sam_files, desc='Converting SAM to BAM'):
        output_file = output_dir / sam_file.with_suffix('.bam').name
        subprocess.run(['samtools', 'view', '-Sb', sam_file, '-o', output_file], check=True)
        logging.info(f'Converted {sam_file} to {output_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert SAM files to BAM format using samtools.',
                                     epilog='Example: python script.py -i /path/to/sam_files -o /path/to/bam_files')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing SAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for BAM files')
    args = parser.parse_args()

    try:
        convert_sam_to_bam(args.input, args.output)
        logging.info("Conversion completed successfully.")
    except Exception as e:
        logging.error(f"Error during conversion: {e}")


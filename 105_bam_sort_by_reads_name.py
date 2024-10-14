import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm

def sort_bam_files(input_dir, output_dir, threads):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bam_files = list(input_dir.glob('*.bam'))
    for bam_file in tqdm(bam_files, desc='Sorting BAM files'):
        output_file = output_dir / (bam_file.stem + '_sort.bam')
        subprocess.run(['samtools', 'sort', '-n', '-@', str(threads), str(bam_file), '-o', str(output_file)], check=True)
        print(f'Sorted {bam_file} to {output_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort BAM files using samtools.',
                                     epilog='Example: python script.py -i /path/to/bam_files -o /path/to/sorted_bam_files -t 8')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for sorted BAM files')
    parser.add_argument('-t', '--threads', type=int, default=8, help='Number of threads to use (default: 8)')
    args = parser.parse_args()

    try:
        sort_bam_files(args.input, args.output, args.threads)
        print("Sorting completed successfully.")
    except Exception as e:
        print(f"Error during sorting: {e}")

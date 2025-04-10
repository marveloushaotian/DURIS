import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm

def coverage_analysis(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bam_files = list(input_dir.glob('*_sort_filter.bam'))
    for bam_file in tqdm(bam_files, desc='Calculating coverage information'):
        output_file = output_dir / (bam_file.stem + '_coverage_info.txt.gz')
        if output_file.exists():
            print(f'Skipping {bam_file.name}, output file already exists.')
            continue
        cmd = ['msamtools', 'coverage', '-z', '--summary', '-o', str(output_file), str(bam_file)]
        subprocess.run(cmd, check=True)
        print(f'Generated coverage information for {bam_file.name} into {output_file.name}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate coverage information for BAM files using msamtools.',
        epilog='Example: python script.py -i /path/to/filtered_bam_files -o /path/to/coverage_info'
    )
    parser.add_argument('-i', '--input', required=True, help='Input directory containing filtered BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for coverage information files')
    args = parser.parse_args()

    try:
        coverage_analysis(args.input, args.output)
        print("Coverage analysis completed successfully.")
    except Exception as e:
        print(f"Error during coverage analysis: {e}")


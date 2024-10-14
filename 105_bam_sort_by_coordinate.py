import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm

def sort_and_index_bam_file(input_file, output_file, threads):
    try:
        # Sort BAM file
        subprocess.run(['samtools', 'sort', '-@', str(threads), str(input_file), '-o', str(output_file)], check=True)
        
        # Index sorted BAM file
        subprocess.run(['samtools', 'index', str(output_file)], check=True)
        
        print(f'Sorted and indexed {input_file} to {output_file}')
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file}: {e}")
        return False

def process_bam_files(input_dir, output_dir, threads):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    bam_files = list(input_dir.glob('*.bam'))
    successful = 0
    failed = 0
    
    for bam_file in tqdm(bam_files, desc='Processing BAM files'):
        output_file = output_dir / (bam_file.stem + '_sort.bam')
        if sort_and_index_bam_file(bam_file, output_file, threads):
            successful += 1
        else:
            failed += 1
    
    return successful, failed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort and index BAM files using samtools.',
                                     epilog='Example: python script.py -i /path/to/bam_files -o /path/to/sorted_bam_files -t 8')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for sorted BAM files')
    parser.add_argument('-t', '--threads', type=int, default=8, help='Number of threads to use (default: 8)')
    args = parser.parse_args()

    try:
        successful, failed = process_bam_files(args.input, args.output, args.threads)
        print(f"Processing completed. Successful: {successful}, Failed: {failed}")
    except Exception as e:
        print(f"Error during processing: {e}")

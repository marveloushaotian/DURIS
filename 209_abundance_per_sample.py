import gzip
import argparse
from pathlib import Path

def process_files(input_file, input_file2, output_file, threshold):
    dictlt = {}
    with gzip.open(input_file, 'rt') as infile:
        for line in infile:
            lst = line.strip().split()
            if float(lst[1]) > threshold:
                dictlt[lst[0]] = lst[0]

    with open(input_file2, 'rt') as infile, open(output_file, 'w') as outfile:
        for i in range(9):
            infile.readline()
        for line in infile:
            lst = line.strip().split()
            try:
                st = "{}\t{}\n".format(dictlt[lst[0]], lst[1])
                outfile.write(st)
            except KeyError:
                st = "{}\t{}\n".format(lst[0], 0)
                outfile.write(st)

def find_pairs(input_dir, threshold):
    input_dir = Path(input_dir)
    coverage_files = list(input_dir.glob('*_coverage_info.txt.gz'))
    profile_files = {f.stem.rstrip('_coverage_info'): f for f in coverage_files}
    
    for profile_base, coverage_file in profile_files.items():
        profile_file = input_dir / (profile_base + '_profile_rb.txt')
        if profile_file.exists():
            output_file = input_dir / (profile_base + '_existing_contigs_ab_per_sample.txt')
            process_files(str(coverage_file), str(profile_file), str(output_file), threshold)

def main():
    parser = argparse.ArgumentParser(description="Process files in pairs with a given threshold.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing the input files.")
    parser.add_argument("-t", "--threshold", type=float, required=True, help="Threshold for contig detection.")
    args = parser.parse_args()

    find_pairs(args.directory, args.threshold)

if __name__ == "__main__":
    main()


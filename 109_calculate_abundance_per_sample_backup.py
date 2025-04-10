import os
import gzip
import argparse

def process_files(input_folder, output_folder, threshold):
    for file_name in os.listdir(input_folder):
        if file_name.endswith("_coverage_info.txt.gz"):
            sample_name = file_name[:-21]
            coverage_file = os.path.join(input_folder, file_name)
            profile_file = os.path.join(input_folder, sample_name + "_profile_rb.txt.gz")
            output_file = os.path.join(output_folder, sample_name + "_existing_contigs_ab_per_sample.txt")

            dictlt = {}
            with gzip.open(coverage_file, 'rt') as infile:
                for line in infile:
                    lst = line.strip().split()
                    if float(lst[1]) > float(threshold):
                        dictlt[lst[0]] = lst[0]

            with gzip.open(profile_file, 'rt') as infile:
                with open(output_file, 'w') as outfile:
                    for i in range(9):
                        infile.readline()
                    for line in infile:
                        lst = line.strip().split()
                        try:
                            st = "{}\t{}\n".format(dictlt[lst[0]], lst[1])
                            outfile.write(st)
                        except:
                            st = "{}\t{}\n".format(lst[0], 0)
                            outfile.write(st)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process coverage and profile files.")
    parser.add_argument("-i", "--input", required=True, help="Input folder containing coverage and profile files.")
    parser.add_argument("-o", "--output", required=True, help="Output folder for processed files.")
    parser.add_argument("-t", "--threshold", type=float, default=0.55, help="Threshold value for coverage (default: 0.0).")
    args = parser.parse_args()

    process_files(args.input, args.output, args.threshold)

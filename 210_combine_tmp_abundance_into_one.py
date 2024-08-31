import os
import argparse
from collections import defaultdict

def linear_paste_relative_contig_abundance(input_files, output_file):
    if os.path.exists(output_file):
        pass
    else:
        dict_ab = defaultdict(str)
        header = "contig_ID"

        for file in input_files:
            sample_ID = os.path.basename(file)[:-len("_existing_contigs_ab_per_sample.txt")]
            header += "\t" + sample_ID
            with open(file, "r") as infile:
                for line in infile:
                    lst = line.strip().split()
                    dict_ab[lst[0]] += "\t" + lst[1]

        with open(output_file, "w") as outfile:
            header += "\n"
            outfile.write(header)
            for k, v in dict_ab.items():
                st = "{}{}\n".format(k, v)
                outfile.write(st)

def main():
    parser = argparse.ArgumentParser(description="Combine contig abundance data from multiple samples.")
    parser.add_argument("-i", "--inputs", nargs='+', required=True, help="Input files (multiple, space separated).")
    parser.add_argument("-o", "--output", required=True, help="Output file path.")
    args = parser.parse_args()

    linear_paste_relative_contig_abundance(args.inputs, args.output)

if __name__ == "__main__":
    main()


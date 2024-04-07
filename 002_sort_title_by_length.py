import argparse
import sys

def sort_by_length(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Sort the lines based on the number following "length_"
    sorted_lines = sorted(lines, key=lambda x: int(x.split('length_')[1].split('_')[0]), reverse=True)

    # Write to the output file
    with open(output_file, 'w') as f:
        f.writelines(sorted_lines)

def main(args):
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Sort lines in a file based on the number following "length_" in descending order.',
        epilog='Example of use: script.py -i all_plasmids.txt -o sorted_plasmids.txt')
    
    parser.add_argument('-i', '--input', required=True, help='Input file containing lines to sort.')
    parser.add_argument('-o', '--output', required=True, help='Output file to write the sorted lines.')

    args = parser.parse_args(args)
    sort_by_length(args.input, args.output)

if __name__ == "__main__":
    main(sys.argv[1:])


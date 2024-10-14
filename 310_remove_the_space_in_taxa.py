import argparse
import csv

def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if row:  # Check if the row is not empty
                # Remove trailing spaces and replace remaining spaces with underscores
                row[0] = row[0].rstrip().replace(' ', '_')
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='Process CSV file: remove trailing spaces and replace remaining spaces with underscores in the first column.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    args = parser.parse_args()

    process_csv(args.input, args.output)
    print(f"Processing complete. Output written to {args.output}")

if __name__ == "__main__":
    main()

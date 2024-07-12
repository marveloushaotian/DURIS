import pandas as pd
import argparse
import gzip

def extract_unique_values_from_csv(csv_file):
    # Read the CSV file and extract unique values from the second column
    df = pd.read_csv(csv_file)
    unique_values = set(df.iloc[:, 1].unique())
    return unique_values

def extract_fasta_sequences(fasta_file, unique_values, output_file):
    with open(fasta_file, 'r') as fasta, open(output_file, 'w') as output:
        write_next_line = False
        for line in fasta:
            if write_next_line:
                output.write(line)
                write_next_line = False
                continue

            if line.startswith('>'):
                # Extract the identifier part from the FASTA header
                identifier = line.split()[0][1:]
                if identifier in unique_values:
                    output.write(line)
                    write_next_line = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract unique values from CSV and match them in FASTA file.")
    parser.add_argument('-c', '--csv', type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument('-f', '--fasta', type=str, required=True, help="Path to the input FASTA file.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to save the extracted FASTA sequences.")

    args = parser.parse_args()

    print("Extracting unique values from CSV file...")
    unique_values = extract_unique_values_from_csv(args.csv)
    print(f"Extracted {len(unique_values)} unique values.")

    print("Extracting sequences from FASTA file...")
    extract_fasta_sequences(args.fasta, unique_values, args.output)
    print(f"Sequences extracted to {args.output}")


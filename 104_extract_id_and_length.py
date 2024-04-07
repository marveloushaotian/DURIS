import argparse
import pandas as pd
from tqdm import tqdm

def extract_length(seqid):
    """Function to extract length from sequence identifier"""
    tokens = seqid.split('_')
    for i, token in enumerate(tokens):
        if token == 'length':
            return int(tokens[i + 1])
    return None

if __name__ == "__main__":
    # Step 2: Argument parser setup with example usage in epilog
    parser = argparse.ArgumentParser(description='Extract length information from sequence identifiers.',
                                     epilog="Example usage: python script_name.py -i your_input_file.txt -o output.csv\nReplace 'script_name.py' with the actual script file name, 'your_input_file.txt' with the path to your input file containing sequence identifiers, and 'output.csv' with your desired output file name.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file containing sequence identifiers.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output CSV file to store the extracted lengths.')

    # Step 3: Parse arguments
    args = parser.parse_args()

    # Read input file
    with open(args.input, 'r') as f:
        lines = f.readlines()

    # Initialize lists to store seqids and lengths
    seqids = []
    lengths = []

    # Loop through each line to extract length
    for line in tqdm(lines, desc="Processing lines"):
        line = line.strip()
        length = extract_length(line)
        if length is not None:
            seqids.append(line)
            lengths.append(length)

    # Create a DataFrame
    df = pd.DataFrame({'seqid': seqids, 'length': lengths})

    # Save the DataFrame to a CSV file
    df.to_csv(args.output, index=False)


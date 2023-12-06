import argparse
import pandas as pd
from tqdm import tqdm

# Step 1: Function to extract length from sequence identifier
def extract_length(seqid):
    tokens = seqid.split('_')
    for i, token in enumerate(tokens):
        if token == 'length':
            return int(tokens[i + 1])
    return None

# Step 2: Argument parser setup
parser = argparse.ArgumentParser(description='Extract length information from sequence identifiers.')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file containing sequence identifiers.')
parser.add_argument('-o', '--output', type=str, required=True, help='Output CSV file to store the extracted lengths.')

# Step 3: Parse arguments
args = parser.parse_args()

# Step 4: Read input file
with open(args.input, 'r') as f:
    lines = f.readlines()

# Step 5: Initialize lists to store seqids and lengths
seqids = []
lengths = []

# Step 6: Loop through each line to extract length
for line in tqdm(lines):
    line = line.strip()
    length = extract_length(line)
    if length is not None:
        seqids.append(line)
        lengths.append(length)

# Step 7: Create a DataFrame
df = pd.DataFrame({'seqid': seqids, 'length': lengths})

# Step 8: Save the DataFrame to a CSV file
df.to_csv(args.output, index=False)


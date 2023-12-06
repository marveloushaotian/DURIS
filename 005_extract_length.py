import pandas as pd
import argparse
from tqdm import tqdm

def process_seqid(seqid):
    """Revised function to extract length and coverage from the seqid string with error handling"""
    try:
        parts = seqid.split("_")
        length_index = parts.index("length") + 1
        cov_index = parts.index("cov") + 1
        length = int(parts[length_index])
        cov = float(parts[cov_index])
        return length, cov
    except (IndexError, ValueError):
        return None, None

def main(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Initialize lists to store extracted values
    length_list = []
    cov_list = []
    
    # Loop through each row in the DataFrame to extract information
    for seqid in tqdm(df['seqid']):
        length, cov = process_seqid(seqid)
        length_list.append(length)
        cov_list.append(cov)
    
    # Add new columns to the DataFrame
    df['length'] = length_list
    df['cov'] = cov_list
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Revised script to split seqid column into length and cov columns")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file")
    args = parser.parse_args()
    
    main(args.input, args.output)


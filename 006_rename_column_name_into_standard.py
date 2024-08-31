import argparse
import pandas as pd
from tqdm import tqdm

def rename_headers(input_file, output_file):
    """
    Rename headers in the first line of the input file according to specified pattern,
    then save the modified content to the output file.
    """
    try:
        # Read the entire file into a DataFrame
        df = pd.read_csv(input_file, sep='\t', header=None)

        # Rename the headers
        new_headers = ['Defense_Name'] + [f'DP_Sample{str(i).zfill(3)}' for i in range(1, len(df.columns))]
        df.iloc[0] = new_headers

        # Save the modified DataFrame back to file
        df.to_csv(output_file, sep='\t', index=False, header=False)
        print("Header renaming completed successfully.")
    except Exception as e:
        print(f"Error during header renaming: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Rename headers in a tab-delimited text file.")
    parser.add_argument('-i', '--input', help="Input file path", required=True)
    parser.add_argument('-o', '--output', help="Output file path", required=True)
    
    args = parser.parse_args()
    
    rename_headers(args.input, args.output)

if __name__ == "__main__":
    main()

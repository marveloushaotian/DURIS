import argparse
import pandas as pd
from tqdm import tqdm

def rename_headers(input_file, output_file):
    try:
        df = pd.read_csv(input_file, sep='\t')

        new_headers = ['Defense_Name'] + [f'Sample_{str(i).zfill(2)}' for i in range(1, len(df.columns))]
        df.columns = new_headers

        df.to_csv(output_file, sep='\t', index=False)
        print("Header renaming completed successfully.")
    except Exception as e:
        print(f"Error during header renaming: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(
        description="Rename headers in a tab-delimited text file.",
        epilog="""
Example:
    python 006_rename_column_name_into_standard.py -i input.txt -o output.txt

This will rename the headers in 'input.txt' and save the result to 'output.txt'.
The first column will be renamed to 'Defense_Name', and subsequent columns will be
renamed to 'Sample_01', 'Sample_02', etc.
        """
    )
    parser.add_argument('-i', '--input', help="Input file path", required=True)
    parser.add_argument('-o', '--output', help="Output file path", required=True)
    
    args = parser.parse_args()
    
    rename_headers(args.input, args.output)

if __name__ == "__main__":
    main()

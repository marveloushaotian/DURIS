import argparse
import os
import pandas as pd
from tqdm import tqdm

def merge_tsv_files(input_path, output_file):
    # 1. Determine input files
    if os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.txt')]
    else:
        files = input_path.split(',')
    
    # 2. Read and merge all files
    dfs = []
    first_columns = None
    for file in tqdm(files, desc="Processing files"):
        df = pd.read_csv(file, sep='\t')
        
        # 3. Check column names
        if first_columns is None:
            first_columns = df.columns
        elif not df.columns.equals(first_columns):
            raise ValueError(f"Column mismatch in file {file}. Expected {list(first_columns)}, got {list(df.columns)}")
        
        dfs.append(df)
    
    # 4. Vertically concatenate all dataframes
    merged_df = pd.concat(dfs, axis=0, ignore_index=True)
    
    # 5. Save the merged file
    merged_df.to_csv(output_file, sep='\t', index=False)
    print(f"Merge completed, saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple tab-separated txt files with identical column names")
    parser.add_argument('-i', '--input_path', required=True, help='Input directory path or comma-separated list of files')
    parser.add_argument('-o', '--output_file', required=True, help='Output file name')
    args = parser.parse_args()

    merge_tsv_files(args.input_path, args.output_file)



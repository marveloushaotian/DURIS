import argparse
import os
import pandas as pd

def merge_tsv_files(input_path, output_file):
    # If input path is a directory, get all txt files
    if os.path.isdir(input_path):
        files = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        files = [os.path.join(input_path, f) for f in files]
    else:
        # If it's a list of files, use it directly
        files = input_path.split(',')
    
    # Read and merge all files
    dfs = []
    for i, file in enumerate(files):
        df = pd.read_csv(file, sep='\t')
        if i > 0:
            # For files after the first one, remove the header
            df = df.iloc[1:]
        dfs.append(df)
    
    # Vertically concatenate all dataframes
    merged_df = pd.concat(dfs, axis=0, ignore_index=True)
    
    # Save the merged file
    merged_df.to_csv(output_file, sep='\t', index=False)
    print(f"Merge completed, saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple tab-separated txt files")
    parser.add_argument('input_path', help='Input directory path or comma-separated list of files')
    parser.add_argument('output_file', help='Output file name')
    args = parser.parse_args()

    merge_tsv_files(args.input_path, args.output_file)

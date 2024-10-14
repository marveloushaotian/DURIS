import pandas as pd
import argparse

def main(input_file, output_file):
    # Read input csv file
    df = pd.read_csv(input_file)
    
    # Sort rows by the second column in descending order 
    df_sorted = df.sort_values(by=df.columns[1], ascending=False)
    
    # Save sorted dataframe to output csv file
    df_sorted.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort rows by the second column in descending order")
    parser.add_argument('-i', '--input', required=True, help="Input csv file path")
    parser.add_argument('-o', '--output', required=True, help="Output csv file path")
    
    args = parser.parse_args()
    main(args.input, args.output)

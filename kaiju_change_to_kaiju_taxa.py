import pandas as pd
import argparse

def main(input_file, output_file):
    # 1. Read the input CSV file
    df = pd.read_csv(input_file)
    
    # 2. Change 'p__Firmicutes' to 'p__Bacillota'
    df.loc[df.iloc[:, 0] == 'p__Firmicutes', df.columns[0]] = 'p__Bacillota'
    
    # 3. Merge rows with 'p__Bacillota' and sum the values
    df_grouped = df.groupby(df.columns[0]).sum().reset_index()
    
    # 4. Save the result to a new CSV file
    df_grouped.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge rows with p__Firmicutes and p__Bacillota")
    parser.add_argument('-i', '--input', required=True, help="Input CSV file path")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file path")
    
    args = parser.parse_args()
    main(args.input, args.output)

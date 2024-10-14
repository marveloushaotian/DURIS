import pandas as pd
import argparse

def main(input_file, output_file):
    # 1. Read the data
    df = pd.read_csv(input_file)
    
    # 2. Group by Contig_ID and merge MGEs_Type, MGEs_SubType, MGEs_Start, and MGEs_End columns
    grouped = df.groupby('Contig_ID').agg({
        'MGEs_Type': lambda x: ';'.join(x),
        'MGEs_SubType': lambda x: ';'.join(x),
        'MGEs_Start': lambda x: ';'.join(map(str, x)),
        'MGEs_End': lambda x: ';'.join(map(str, x))
    }).reset_index()
    
    # 3. Calculate MGEs_Number column
    grouped['MGEs_Number'] = df.groupby('Contig_ID').size().reset_index(name='count')['count']
    
    # 4. Save the result to a new file
    grouped.to_csv(output_file, index=False)
    
    print(f"Data has been successfully combined and saved to '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine MGEs info data.")
    
    # Input file argument
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the input CSV file")
    
    # Output file argument
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output CSV file")
    
    args = parser.parse_args()
    
    main(args.input, args.output)

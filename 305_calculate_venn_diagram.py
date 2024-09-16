import pandas as pd
import argparse
from pathlib import Path
import os

def process_csv(input_file, output_dir, group_by='Location', defense_column='Defense_Type'):
    # 1. Read the CSV file
    df = pd.read_csv(input_file)
    
    # 2. Group by the specified column
    grouped = df.groupby(group_by)
    
    # 3. Process each group
    for name, group in grouped:
        # Get unique Defense_Type values
        unique_defenses = group[defense_column].unique()
        
        # Filter out unwanted prefixes and 'No' value
        filtered_defenses = [d for d in unique_defenses if not d.startswith(('HEC_', 'PDC_', 'DMS_')) and d != 'No']
        
        # Create a DataFrame with the filtered defenses
        result_df = pd.DataFrame({defense_column: filtered_defenses})
        
        # Create output file name
        output_file = os.path.join(output_dir, f"{name}.csv")
        
        # Save to CSV
        result_df.to_csv(output_file, index=False)
        print(f"Results for {name} saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Process CSV and group by specified column.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output directory path')
    parser.add_argument('-g', '--group_by', default='Location', help='Column to group by (default: Location)')
    parser.add_argument('-d', '--defense_column', default='Defense_Type', help='Column containing defense types (default: Defense_Type)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    # Process the CSV file
    process_csv(args.input, args.output, args.group_by, args.defense_column)

if __name__ == "__main__":
    main()

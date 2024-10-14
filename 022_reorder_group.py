import pandas as pd
import argparse

def custom_sort(df):
    # Define custom sort orders
    location_order = ['HP', 'RS', 'MS', 'BTP']
    country_order = ['DK', 'SP', 'UK']
    classification_order = ['Chromosome', 'Plasmid', 'Phage']
    
    # Create sorting keys based on available columns
    sort_columns = []
    
    if 'Location' in df.columns:
        df['Location_sort'] = pd.Categorical(df['Location'], categories=location_order, ordered=True)
        sort_columns.append('Location_sort')
    
    if 'Country' in df.columns:
        df['Country_sort'] = pd.Categorical(df['Country'], categories=country_order, ordered=True)
        sort_columns.append('Country_sort')
    
    if 'Contig_Classification' in df.columns:
        df['Classification_sort'] = pd.Categorical(df['Contig_Classification'], categories=classification_order, ordered=True)
        sort_columns.append('Classification_sort')
    
    # Sort the dataframe
    df_sorted = df.sort_values(sort_columns)
    
    # Remove temporary sorting columns
    df_sorted = df_sorted.drop(columns=[col for col in df_sorted.columns if col.endswith('_sort')])
    
    return df_sorted

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Sort a CSV file based on specific column orders.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')
    args = parser.parse_args()

    # Read the input CSV file
    df = pd.read_csv(args.input)

    # Apply custom sorting
    df_sorted = custom_sort(df)

    # Save the sorted dataframe to a new CSV file
    df_sorted.to_csv(args.output, index=False)
    print(f"Sorted data has been saved to {args.output}")

if __name__ == "__main__":
    main()

# Usage example:
# python script_name.py -i input_file.csv -o output_file.csv

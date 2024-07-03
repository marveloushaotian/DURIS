import pandas as pd
import argparse

def merge_and_aggregate(file1, file2, output_file):
    # Load the data
    data1 = pd.read_csv(file1, sep='\t', header=None, skiprows=1)
    data2 = pd.read_csv(file2, sep='\t', header=None)
    
    # Assuming the first column of data1 is 'contig_ID' and the rest are numerical values
    headers = ['contig_ID'] + [f'Value_{i}' for i in range(1, data1.shape[1])]
    data1.columns = headers
    data2.columns = ['contig_ID', 'Taxonomy']

    # Merge the data on 'contig_ID'
    merged_data = pd.merge(data1, data2, on='contig_ID', how='left')
    
    # Replace 'contig_ID' with 'Taxonomy' names
    merged_data['contig_ID'] = merged_data['Taxonomy']
    del merged_data['Taxonomy']  # Remove the taxonomy column as it's now redundant

    # Aggregate the data by new 'contig_ID' (which are now Taxonomy names)
    # This will sum all numerical columns that share the same Taxonomy name
    aggregated_data = merged_data.groupby('contig_ID').sum()
    aggregated_data.reset_index(inplace=True)  # Turn the index back into a column

    # Re-assign original headers to maintain column names (except for the 'contig_ID' which is now 'Taxonomy')
    new_headers = ['Taxonomy'] + headers[1:]  # 'Taxonomy' replaces 'contig_ID'
    aggregated_data.columns = new_headers

    # Save the aggregated data to a new file
    aggregated_data.to_csv(output_file, sep='\t', index=False)

def main():
    parser = argparse.ArgumentParser(description="Merge two files on 'contig_ID', replace with taxonomy, and aggregate numerically while preserving original column names.")
    parser.add_argument("-f1", "--file1", required=True, help="Path to the first input file (contig data).")
    parser.add_argument("-f2", "--file2", required=True, help="Path to the second input file (taxonomy data).")
    parser.add_argument("-o", "--output", required=True, help="Output file path.")
    args = parser.parse_args()

    merge_and_aggregate(args.file1, args.file2, args.output)

if __name__ == "__main__":
    main()


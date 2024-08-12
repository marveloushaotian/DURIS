import pandas as pd
import argparse
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_columns(column_input, df):
    """Parse the column input, which can be column names or column indices."""
    if all(col.isdigit() for col in column_input):
        # Interpret as column indices
        col_indices = list(map(int, column_input))
        columns = df.columns[col_indices].tolist()
    else:
        # Interpret as column names
        columns = column_input
    return columns

def merge_files(main_file, main_col, aux_file, aux_col, aux_cols_to_add, output_file):
    # Load the main file and auxiliary file
    try:
        main_df = pd.read_csv(main_file, sep='\t')
        aux_df = pd.read_csv(aux_file, sep='\t')
    except Exception as e:
        logging.error(f"Error reading files: {e}")
        sys.exit(1)
    
    # Check if the columns exist
    if main_col not in main_df.columns:
        logging.error(f"Main column '{main_col}' not found in main file.")
        sys.exit(1)
    
    if aux_col not in aux_df.columns:
        logging.error(f"Auxiliary column '{aux_col}' not found in auxiliary file.")
        sys.exit(1)
    
    # Parse the auxiliary columns to add
    aux_cols_to_add_parsed = parse_columns(aux_cols_to_add, aux_df)
    
    missing_cols = [col for col in aux_cols_to_add_parsed if col not in aux_df.columns]
    if missing_cols:
        logging.error(f"Columns {missing_cols} not found in auxiliary file.")
        sys.exit(1)
    
    # Merge the files
    merged_df = pd.merge(main_df, aux_df[[aux_col] + aux_cols_to_add_parsed], left_on=main_col, right_on=aux_col, how='left')
    
    # Rename the auxiliary column to match the main column if they are different
    if main_col != aux_col:
        merged_df.drop(columns=[aux_col], inplace=True)
    
    # Save the result to a new file
    try:
        merged_df.to_csv(output_file, sep='\t', index=False)
        logging.info(f"Successfully saved the merged file to {output_file}")
    except Exception as e:
        logging.error(f"Error saving the merged file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two tab-separated files based on a matching column, and add specified columns from the auxiliary file to the main file. Columns can be specified by name or by index (starting from 0).")

    # Add arguments
    parser.add_argument("-m", "--main_file", required=True, help="Path to the main file (tab-separated).")
    parser.add_argument("-mc", "--main_col", required=True, help="Column name in the main file to match.")
    parser.add_argument("-a", "--aux_file", required=True, help="Path to the auxiliary file (tab-separated).")
    parser.add_argument("-ac", "--aux_col", required=True, help="Column name in the auxiliary file to match.")
    parser.add_argument("-c", "--aux_cols_to_add", required=True, nargs='+', help="Column names or indices in the auxiliary file to add to the main file. For indices, use numbers starting from 0.")
    parser.add_argument("-o", "--output_file", required=True, help="Path to save the output merged file (tab-separated).")

    # Parse arguments
    args = parser.parse_args()

    # Call the merge function
    merge_files(args.main_file, args.main_col, args.aux_file, args.aux_col, args.aux_cols_to_add, args.output_file)


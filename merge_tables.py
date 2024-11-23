import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def merge_csv(
    input_file_1, input_file_2, match_column_1, match_column_2, columns_to_add, output_file
):
    """
    Merge two CSV files based on matching columns, adding specified columns to the output.

    Args:
        input_file_1 (str): Path to the first CSV file.
        input_file_2 (str): Path to the second CSV file.
        match_column_1 (str): Column in the first file to match on.
        match_column_2 (str): Column in the second file to match on.
        columns_to_add (list): Columns from the second file to add to the first file.
        output_file (str): Path to the output CSV file.
    """
    logging.info("Loading input files...")
    df1 = pd.read_csv(input_file_1)
    df2 = pd.read_csv(input_file_2)

    logging.info("Preparing merge operation...")
    tqdm.pandas()  # Enable progress bar for pandas

    # Subset df2 to include only the matching column and columns to add
    merge_columns = [match_column_2] + columns_to_add
    df2_subset = df2[merge_columns]

    # Merge the dataframes
    logging.info("Performing merge operation...")
    merged_df = df1.merge(
        df2_subset,
        left_on=match_column_1,
        right_on=match_column_2,
        how="left",
    )

    # Save the result
    logging.info("Saving merged output...")
    merged_df.to_csv(output_file, index=False)
    logging.info(f"Merged file saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Merge two CSV files based on matching columns and add specified columns to the output."
    )
    parser.add_argument("-i1", "--input_file_1", required=True, help="Path to the first CSV file.")
    parser.add_argument("-i2", "--input_file_2", required=True, help="Path to the second CSV file.")
    parser.add_argument("-m1", "--match_column_1", required=True, help="Matching column in the first file.")
    parser.add_argument("-m2", "--match_column_2", required=True, help="Matching column in the second file.")
    parser.add_argument(
        "-c", "--columns_to_add", required=True, nargs="+", help="Columns to add from the second file."
    )
    parser.add_argument("-o", "--output_file", required=True, help="Path to the output CSV file.")

    # Parse arguments
    args = parser.parse_args()

    # Call the merge function
    merge_csv(
        args.input_file_1,
        args.input_file_2,
        args.match_column_1,
        args.match_column_2,
        args.columns_to_add,
        args.output_file,
    )


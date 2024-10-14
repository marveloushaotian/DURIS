import argparse
import pandas as pd
from tqdm import tqdm

# Function to rename and reorder columns
def rename_and_reorder_headers(input_file, output_file):
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)

        # Step 1: Rename the columns
        new_headers = ['Contig_ID'] + [f'Sample_{str(i).zfill(2)}' for i in range(1, len(df.columns))]
        df.columns = new_headers

        # Step 2: Reorder the 'Sample_' columns according to the given order
        sample_order = [
            "Sample_01", "Sample_02", "Sample_06", "Sample_07", "Sample_11", "Sample_12", "Sample_40", "Sample_41",
            "Sample_45", "Sample_46", "Sample_50", "Sample_51", "Sample_28", "Sample_32", "Sample_36", "Sample_67",
            "Sample_71", "Sample_75", "Sample_16", "Sample_20", "Sample_24", "Sample_55", "Sample_59", "Sample_63",
            "Sample_03", "Sample_08", "Sample_13", "Sample_42", "Sample_47", "Sample_52", "Sample_29", "Sample_33",
            "Sample_37", "Sample_68", "Sample_72", "Sample_76", "Sample_17", "Sample_21", "Sample_25", "Sample_56",
            "Sample_60", "Sample_64", "Sample_04", "Sample_09", "Sample_14", "Sample_43", "Sample_48", "Sample_53",
            "Sample_30", "Sample_34", "Sample_38", "Sample_69", "Sample_73", "Sample_77", "Sample_18", "Sample_22",
            "Sample_26", "Sample_57", "Sample_61", "Sample_65", "Sample_05", "Sample_10", "Sample_15", "Sample_44",
            "Sample_49", "Sample_54", "Sample_31", "Sample_35", "Sample_39", "Sample_70", "Sample_74", "Sample_78",
            "Sample_19", "Sample_23", "Sample_27", "Sample_58", "Sample_62", "Sample_66"
        ]

        # Get non-sample columns and sample columns in the given order
        non_sample_columns = ['Contig_ID']
        sample_columns = [col for col in sample_order if col in df.columns]

        # Ensure final column order is correct
        final_columns = non_sample_columns + sample_columns
        df = df[final_columns]

        # Step 3: Save the reordered DataFrame to the output file
        df.to_csv(output_file, index=False)
        print("Header renaming and reordering completed successfully.")
    except Exception as e:
        print(f"Error during header renaming and reordering: {e}")
        raise

# Main function to handle argument parsing
def main():
    parser = argparse.ArgumentParser(
        description="Rename headers in a CSV file and reorder columns.",
        epilog="""
Example:
    python script.py -i input.csv -o output.csv

This will rename the headers in 'input.csv', reorder the 'Sample_' columns as per the specified order, and save the result to 'output.csv'.
        """
    )
    parser.add_argument('-i', '--input', help="Input CSV file path", required=True)
    parser.add_argument('-o', '--output', help="Output CSV file path", required=True)
    
    args = parser.parse_args()
    
    rename_and_reorder_headers(args.input, args.output)

if __name__ == "__main__":
    main()

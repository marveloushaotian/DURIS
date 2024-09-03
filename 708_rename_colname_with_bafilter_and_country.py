import os
import pandas as pd
import argparse

def reorder_columns(input_dir, output_dir, column_order, id_column='Type'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get a list of all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  # Change this to match your file extension
            input_file_path = os.path.join(input_dir, filename)
            
            # Load the data
            data = pd.read_csv(input_file_path, sep='\t')

            # Create the new order including the ID column
            new_order = [id_column] + column_order

            # Reorder the columns
            reordered_data = data[new_order]

            # Save the reordered data to a new file in the output directory
            output_file_path = os.path.join(output_dir, filename)
            reordered_data.to_csv(output_file_path, sep='\t', index=False)
            print(f"Reordered file saved: {output_file_path}")

if __name__ == "__main__":
    # Define the column order
    column_order = [
        "Sample_01", "Sample_02", "Sample_03", "Sample_04", "Sample_06", "Sample_07", "Sample_08", "Sample_09",
        "Sample_11", "Sample_12", "Sample_13", "Sample_14", "Sample_40", "Sample_41", "Sample_42", "Sample_43",
        "Sample_45", "Sample_46", "Sample_47", "Sample_48", "Sample_50", "Sample_51", "Sample_52", "Sample_53",
        "Sample_28", "Sample_29", "Sample_30", "Sample_32", "Sample_33", "Sample_34", "Sample_36", "Sample_37",
        "Sample_38", "Sample_67", "Sample_68", "Sample_69", "Sample_71", "Sample_72", "Sample_73", "Sample_75",
        "Sample_76", "Sample_77", "Sample_16", "Sample_17", "Sample_18", "Sample_20", "Sample_21", "Sample_22",
        "Sample_24", "Sample_25", "Sample_26", "Sample_55", "Sample_56", "Sample_57", "Sample_59", "Sample_60",
        "Sample_61", "Sample_63", "Sample_64", "Sample_65", "Sample_05", "Sample_10", "Sample_15", "Sample_44",
        "Sample_49", "Sample_54", "Sample_31", "Sample_35", "Sample_39", "Sample_70", "Sample_74", "Sample_78",
        "Sample_19", "Sample_23", "Sample_27", "Sample_58", "Sample_62", "Sample_66"
    ]

    # Define argument parser
    parser = argparse.ArgumentParser(description="Reorder columns in CSV files.")
    
    # Required arguments
    parser.add_argument('-i', '--input_dir', type=str, required=True, help="Directory containing the input files.")
    parser.add_argument('-o', '--output_dir', type=str, required=True, help="Directory to save the output files.")
    
    # Optional arguments
    parser.add_argument('--id_column', type=str, default='Type', help="Name of the ID column that stays first.")
    
    # Parse arguments
    args = parser.parse_args()

    # Call the reorder function
    reorder_columns(args.input_dir, args.output_dir, column_order, args.id_column)


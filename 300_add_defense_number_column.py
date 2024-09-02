import pandas as pd

def add_defense_number_column(input_file, output_file):
    # Read the file into a DataFrame
    df = pd.read_csv(input_file, sep="\t")
    
    # Add Defense_Number column, set to 1 when Defense_Type is not empty, otherwise empty
    df['Defense_Number'] = df['Defense_Type'].apply(lambda x: 1 if pd.notna(x) else '')
    
    # Write the result to the output file
    df.to_csv(output_file, sep="\t", index=False)

if __name__ == "__main__":
    import argparse

    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Add Defense_Number column to the file based on Defense_Type.")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the All_contigs_info_without_PDC_single_defense.txt file.")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output file.")

    args = parser.parse_args()

    # Call the function to add Defense_Number column
    add_defense_number_column(args.input_file, args.output_file)

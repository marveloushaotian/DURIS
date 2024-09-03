import pandas as pd
import argparse

def main(input_file, output_file, classification):
    # Read the input file
    df = pd.read_csv(input_file, sep='\t')
    
    # Filter rows based on Contig_Classification
    df_filtered = df[df['Contig_Classification'] == classification]
    
    # Extract the required columns
    df_filtered = df_filtered[['Contig_ID', 'Defense_Subtype', 'Sample']]
    
    # Count occurrences of each Defense_Subtype for each Sample
    count_df = df_filtered.groupby(['Defense_Subtype', 'Sample']).size().unstack(fill_value=0)
    
    # Define the desired order of Sample columns
    desired_order = [
        "Sample_01", "Sample_02", "Sample_03", "Sample_04", "Sample_06", "Sample_07", "Sample_08", "Sample_09",
        "Sample_11", "Sample_12", "Sample_13", "Sample_14", "Sample_16", "Sample_17", "Sample_18", "Sample_20",
        "Sample_21", "Sample_22", "Sample_24", "Sample_25", "Sample_26", "Sample_28", "Sample_29", "Sample_30",
        "Sample_32", "Sample_33", "Sample_34", "Sample_36", "Sample_37", "Sample_38", "Sample_40", "Sample_41",
        "Sample_42", "Sample_43", "Sample_45", "Sample_46", "Sample_47", "Sample_48", "Sample_50", "Sample_51",
        "Sample_52", "Sample_53", "Sample_55", "Sample_56", "Sample_57", "Sample_59", "Sample_60", "Sample_61",
        "Sample_63", "Sample_64", "Sample_65", "Sample_67", "Sample_68", "Sample_69", "Sample_71", "Sample_72",
        "Sample_73", "Sample_75", "Sample_76", "Sample_77", "Sample_05", "Sample_10", "Sample_15", "Sample_19",
        "Sample_23", "Sample_27", "Sample_31", "Sample_35", "Sample_39", "Sample_44", "Sample_49", "Sample_54",
        "Sample_58", "Sample_62", "Sample_66", "Sample_70", "Sample_74", "Sample_78"
    ]
    
    # Reindex the DataFrame to match the desired order of columns
    count_df = count_df.reindex(columns=desired_order, fill_value=0)
    
    # Save the result to a txt file
    count_df.to_csv(output_file, sep='\t')
    
    print(f"Conversion complete. The result is saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process defense info data.")
    
    # Input file argument
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the input file")
    
    # Output file argument
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output file")
    
    # Classification filter argument
    parser.add_argument('-c', '--classification', type=str, required=True, choices=['Chromosome', 'Plasmid'],
                        help="Contig classification to filter by (Chromosome or Plasmid)")
    
    args = parser.parse_args()
    
    main(args.input, args.output, args.classification)


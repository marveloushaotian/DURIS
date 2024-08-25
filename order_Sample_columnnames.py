import pandas as pd
import argparse
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义Sample列的顺序
sample_order = [
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

def reorder_sample_columns(input_file, output_file):
    # Load the data
    logging.info(f'Loading data from {input_file}')
    df = pd.read_csv(input_file, sep='\t')
    
    # Separate Sample_ columns and other columns
    sample_columns = [col for col in df.columns if col.startswith("Sample_")]
    other_columns = [col for col in df.columns if not col.startswith("Sample_")]
    
    # Reorder Sample_ columns according to the predefined order
    reordered_sample_columns = [col for col in sample_order if col in sample_columns]
    missing_columns = [col for col in sample_columns if col not in sample_order]
    
    # Append missing Sample_ columns to the reordered list
    reordered_sample_columns.extend(missing_columns)
    
    # Create a new DataFrame with the columns reordered
    final_columns = other_columns + reordered_sample_columns
    reordered_df = df[final_columns]
    
    # Save the reordered DataFrame to a new file
    logging.info(f'Saving reordered data to {output_file}')
    reordered_df.to_csv(output_file, sep='\t', index=False)
    logging.info('Done!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reorder Sample_ columns in a txt file.')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    reorder_sample_columns(args.input, args.output)


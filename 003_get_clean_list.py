import pandas as pd
from tqdm import tqdm
import argparse
import logging

# Initialize logging
logging.basicConfig(filename='processing.log', level=logging.INFO)

# Define a function to process the CSV file
def process_csv(input_file, output_file):
    # Step 1: Remove duplicate headers and metadata
    logging.info("Step 1: Removing duplicate headers and metadata.")
    df = pd.read_csv(input_file)
    df = df[df['system.number'] != 'system.number']
    
    # Step 2: Keep only the first occurrence of each specified field
    logging.info("Step 2: Keeping only the first occurrence of each specified field.")
    specified_fields = ['system.number', 'seqid', 'system', 'target.name', 'hmm.accession',
                        'hmm.name', 'protein.name', 'full.seq.E.value', 'domain.iE.value',
                        'target.coverage', 'hmm.coverage', 'start', 'end', 'strand',
                        'target.description', 'relative.position', 'contig.end', 'all.domains', 'best.hits']
    df = df.drop_duplicates(subset=specified_fields)
    
    # Step 3: Save the processed DataFrame
    logging.info("Step 3: Saving the processed DataFrame.")
    df.to_csv(output_file, index=False)
    
    logging.info("Processing completed.")

# Define main function to utilize argparse
def main():
    parser = argparse.ArgumentParser(description='处理一个不重复的防御列表CSV文件。')
    parser.add_argument('-i', '--input', help='输入CSV文件路径', required=True)
    parser.add_argument('-o', '--output', help='输出CSV文件路径', required=True)
    
    args = parser.parse_args()
    
    process_csv(args.input, args.output)

if __name__ == "__main__":
    main()

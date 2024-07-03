import csv
from Bio import SeqIO
import argparse

def extract_sequences(csv_file, fasta_file, output_file):
    # Read the CSV file
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Skip the header row
        
        seq_info = {}
        for row in csv_reader:
            seqid = row[1]
            target_name = row[3]
            start = int(row[11])
            end = int(row[12])
            
            if seqid not in seq_info:
                seq_info[seqid] = []
            seq_info[seqid].append((target_name, start, end))
    
    # Read the FASTA file and extract sequences
    sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, 'fasta'))
    
    with open(output_file, 'w') as outfile:
        for seqid, details in seq_info.items():
            if seqid in sequences:
                sequence = str(sequences[seqid].seq)
                for target_name, start, end in details:
                    extracted_sequence = sequence[start-1:end]  # Extract the substring
                    outfile.write(f'>{target_name}\n')
                    outfile.write(f'{extracted_sequence}\n')
            else:
                print(f'seqid not found in FASTA file: {seqid}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract sequence segments from a FASTA file based on information from a CSV file.")
    parser.add_argument('-c', '--csv_file', required=True, help="Path to the input CSV file")
    parser.add_argument('-f', '--fasta_file', required=True, help="Path to the input FASTA file")
    parser.add_argument('-o', '--output_file', required=True, help="Path to the output file")

    args = parser.parse_args()
    
    extract_sequences(args.csv_file, args.fasta_file, args.output_file)


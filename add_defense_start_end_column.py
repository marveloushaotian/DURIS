import pandas as pd
import argparse

def merge_files(expanded_file, padloc_file, output_file):
    # Read files
    expanded_df = pd.read_csv(expanded_file, sep='\t')
    padloc_df = pd.read_csv(padloc_file, sep='\t')[['seqid', 'system', 'start', 'end']]

    # Merge files
    merged_df = pd.merge(expanded_df, padloc_df, 
                         left_on=['Contig_ID', 'Defense_Subtype'], 
                         right_on=['seqid', 'system'], 
                         how='left')

    # Process merged dataframe
    merged_df.rename(columns={'start': 'Start', 'end': 'End'}, inplace=True)
    merged_df.drop(columns=['seqid', 'system'], inplace=True)
    merged_df[['Start', 'End']] = merged_df[['Start', 'End']].fillna('.')

    # Save to new file
    merged_df.to_csv(output_file, sep='\t', index=False)

def main():
    parser = argparse.ArgumentParser(description="Merge defense info with PADLOC data")
    parser.add_argument('-e', '--expanded', help="Expanded_defense_info.txt file")
    parser.add_argument('-p', '--padloc', help="PADLOC.txt file")
    parser.add_argument('-o', '--output', help="Output file")
    args = parser.parse_args()

    merge_files(args.expanded, args.padloc, args.output)

if __name__ == "__main__":
    main()

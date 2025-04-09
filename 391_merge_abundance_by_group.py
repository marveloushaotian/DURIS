import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

def main():
    # 1. Parse command line arguments
    parser = argparse.ArgumentParser(description="Merge and average samples in a CSV file based on grouping information.")
    parser.add_argument('-i', '--input', required=True, help="Input CSV file (file a)")
    parser.add_argument('-g', '--grouping', required=True, help="Grouping CSV file (file b)")
    parser.add_argument('-c', '--columns', required=True, nargs='+', help="Columns in grouping file to use for grouping")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file")
    args = parser.parse_args()

    # 2. Read input files
    df_a = pd.read_csv(args.input, index_col='Contig_ID')
    df_b = pd.read_csv(args.grouping, index_col='Sample')

    # 3. Create grouping dictionary and ordered groups
    grouping = df_b[args.columns].apply(lambda x: '_'.join(x.astype(str)), axis=1)
    group_dict = grouping.to_dict()
    ordered_groups = grouping.drop_duplicates().tolist()

    # 4. Group and average samples
    new_data = []

    for group in tqdm(ordered_groups, desc="Processing groups"):
        samples = [sample for sample, g in group_dict.items() if g == group]
        if samples:
            new_data.append(df_a[samples].mean(axis=1))

    # 5. Create and save the new dataframe
    df_result = pd.DataFrame(np.column_stack(new_data), index=df_a.index, columns=ordered_groups)
    df_result.to_csv(args.output)

    print(f"Grouped and averaged data saved to {args.output}")

if __name__ == "__main__":
    main()

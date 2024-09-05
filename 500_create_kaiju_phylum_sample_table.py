import pandas as pd
import argparse

def main(input_file, output_file):
    # 读取文件
    df = pd.read_csv(input_file, sep='\t')
    
    # 提取 Sample 和 Phylum 列
    df_extracted = df[['Sample', 'Phylum']]
    
    # 创建透视表，每列是一个 Sample，每行是一个 Phylum，单元格中的数字是条目的数量
    pivot_table = df_extracted.pivot_table(index='Phylum', columns='Sample', aggfunc='size', fill_value=0)
    
    # 保存到新的文件
    pivot_table.to_csv(output_file, sep='\t')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a table with Samples as columns and Phylums as rows, with counts as values")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output file path")
    
    args = parser.parse_args()
    main(args.input, args.output)


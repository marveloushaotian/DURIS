import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用Agg后端，可能有助于解决一些渲染问题
import matplotlib.pyplot as plt
import argparse

def create_stacked_bar_chart(input_file, output_file):
    df = pd.read_csv(input_file, sep='\t')
    grouped = df.groupby(['Defense_Type', 'Contig_Group']).size().unstack(fill_value=0)
    total_counts = grouped.sum(axis=1).sort_values(ascending=False)
    top_30_defense_types = total_counts.head(30).index
    grouped = grouped.loc[top_30_defense_types]
    
    custom_colors = ["#4a9ba7", "#9bb88a", "#d0cab7", "#c6a4c5", "#434d91", "#e1834e", "#cd6073", "#ffc7c9"]
    
    fig, ax = plt.subplots(figsize=(20, 10))  # 明确创建图形和轴对象
    
    grouped.plot(kind='bar', stacked=True, color=custom_colors, edgecolor='black', linewidth=0.5, ax=ax)
    
    plt.ylabel('Defense Number')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Contig Group', loc='upper right', bbox_to_anchor=(0.99, 0.99), 
               frameon=False, fontsize='small')
    plt.xlabel('')
    
    plt.subplots_adjust(bottom=0.2)  # 增加底部边距，防止x轴标签被截断
    
    # 确保图形大小正确
    fig.set_size_inches(12, 8)
    
    # 保存图形，不使用bbox_inches='tight'
    plt.savefig(output_file, format='pdf', dpi=300)
    plt.close(fig)  # 明确关闭图形

def main():
    parser = argparse.ArgumentParser(description='Create a stacked bar chart showing the frequency of each Defense Type by Contig Group.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output PDF file')
    args = parser.parse_args()
    
    create_stacked_bar_chart(args.input, args.output)

if __name__ == '__main__':
    main()

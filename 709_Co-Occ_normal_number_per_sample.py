import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import argparse

def main(input_file, output_image, output_table, element_column, group_column):
    # 预定义的列名
    defense_column = 'Defense_Type'
    location_column = 'Location_BAF'
    sample_column = 'Sample'

    # Step 1: 读取数据
    df = pd.read_csv(input_file, sep='\t')

    # Step 2: 数据过滤
    filtered_df = df[(df[element_column].notna()) & (df[element_column] != 'No') &
                     (df[defense_column].notna()) & (df[defense_column] != 'No')]

    # Step 3: 数据分组与计数
    grouped_df = filtered_df.groupby([group_column, location_column, sample_column]).size().reset_index(name='Count')

    # Step 4: 调整Location_BAF顺序
    grouped_df[location_column] = pd.Categorical(grouped_df[location_column], categories=['Before_Filter', 'After_Filter'], ordered=True)

    # Step 5: 设置颜色
    palette = {"Before_Filter": "#b58db3", "After_Filter": "#75b989"}

    # Step 6: 绘制Boxplot
    plt.figure(figsize=(6, 8))
    sns.boxplot(x=group_column, y='Count', hue=location_column, data=grouped_df, dodge=True, palette=palette)
    sns.stripplot(x=group_column, y='Count', hue=location_column, data=grouped_df, dodge=True, jitter=True, color='black', marker='o', alpha=0.5)

    # Step 7: 显著性检验
    groups = grouped_df[group_column].unique()
    for group in groups:
        before_filter = grouped_df[(grouped_df[group_column] == group) & (grouped_df[location_column] == 'Before_Filter')]['Count']
        after_filter = grouped_df[(grouped_df[group_column] == group) & (grouped_df[location_column] == 'After_Filter')]['Count']
        if len(before_filter) > 0 and len(after_filter) > 0:
            stat, p_value = ttest_ind(before_filter, after_filter, equal_var=False)
            y_max = max(before_filter.max(), after_filter.max())
            plt.text(groups.tolist().index(group), y_max + 1, f'p={p_value:.3f}', ha='center')

    # Step 8: 图形美化
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=0, ha='center')
    plt.legend(title=location_column, bbox_to_anchor=(0.99, 0.99), loc='upper left')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tight_layout()

    # Step 9: 保存图片
    plt.savefig(output_image, dpi=300)
    plt.show()

    # Step 10: 输出统计结果表
    grouped_df.to_csv(output_table, index=False, sep='\t')
    print(f"Results saved to {output_table}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze genomic elements and output a plot and table.')

    # 输入和输出文件参数
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path (tab-separated).')
    parser.add_argument('-o', '--output_image', type=str, required=True, help='Output image file path.')
    parser.add_argument('-t', '--output_table', type=str, required=True, help='Output table file path.')

    # 可变参数
    parser.add_argument('-e', '--element_column', type=str, required=True, help='Column name for the element (e.g., Transposon, Integron).')
    parser.add_argument('-g', '--group_column', type=str, required=True, help='Column name for the group (e.g., Country).')

    args = parser.parse_args()

    # 调用主函数
    main(input_file=args.input, output_image=args.output_image, output_table=args.output_table,
         element_column=args.element_column, group_column=args.group_column)


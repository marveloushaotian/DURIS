import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import argparse

def main(input_file, output_image, output_table, elements, group_column):
    # 预定义的列名
    defense_column = 'Defense_Type'
    location_column = 'Location_BAF'
    sample_column = 'Sample'
    
    # 初始化一个空的DataFrame来存储所有元素的结果
    combined_df = pd.DataFrame()

    for element_column in elements:
        # Step 2: 数据过滤
        filtered_df = df[(df[element_column].notna()) & (df[element_column] != 'No') &
                         (df[defense_column].notna()) & (df[defense_column] != 'No')]

        # Step 3: 数据分组与计数
        grouped_df = filtered_df.groupby([group_column, location_column, sample_column]).size().reset_index(name='Count')
        grouped_df['Element'] = element_column  # 添加一列用于标记元素类型
        
        # 确保没有重复的索引
        grouped_df = grouped_df.reset_index(drop=True)
        
        # 将当前元素的数据追加到总的DataFrame中
        combined_df = pd.concat([combined_df, grouped_df])

    # Step 4: 调整Location_BAF顺序
    combined_df[location_column] = pd.Categorical(combined_df[location_column], categories=['Before_Filter', 'After_Filter'], ordered=True)

    # Step 5: 设置颜色
    palette = {"Before_Filter": "#b58db3", "After_Filter": "#75b989"}

    # Step 6: 绘制FacetGrid图
    g = sns.catplot(
        x=group_column, y='Count', hue=location_column, col='Element',
        data=combined_df, kind='box', palette=palette, dodge=True,
        height=5, aspect=1.2
    )
    # 为每个子图设置stripplot，显式指定顺序
    for ax in g.axes.flat:
        sns.stripplot(
            x=group_column, y='Count', hue=location_column, data=combined_df, 
            dodge=True, jitter=True, color='black', marker='o', alpha=0.5, order=sorted(combined_df[group_column].unique()), ax=ax
        )

    # Step 7: 显著性检验并标注
    for ax, element_column in zip(g.axes.flat, elements):
        element_df = combined_df[combined_df['Element'] == element_column]
        groups = element_df[group_column].unique()
        for group in groups:
            before_filter = element_df[(element_df[group_column] == group) & (element_df[location_column] == 'Before_Filter')]['Count']
            after_filter = element_df[(element_df[group_column] == group) & (element_df[location_column] == 'After_Filter')]['Count']
            if len(before_filter) > 0 and len(after_filter) > 0:
                stat, p_value = ttest_ind(before_filter, after_filter, equal_var=False)
                y_max = max(before_filter.max(), after_filter.max())
                ax.text(groups.tolist().index(group), y_max + 1, f'p={p_value:.3f}', ha='center')

    # Step 8: 图形美化
    g.set_axis_labels("", "Count")
    g.set_titles(col_template="{col_name}")
    g.despine(left=True)
    plt.tight_layout()

    # Step 9: 保存图片
    plt.savefig(output_image, dpi=300)
    plt.show()

    # Step 10: 输出统计结果表
    combined_df.to_csv(output_table, index=False, sep='\t')
    print(f"Results saved to {output_table}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze multiple genomic elements and output a plot and table.')

    # 输入和输出文件参数
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path (tab-separated).')
    parser.add_argument('-o', '--output_image', type=str, required=True, help='Output image file path.')
    parser.add_argument('-t', '--output_table', type=str, required=True, help='Output table file path.')

    # 可变参数
    parser.add_argument('-e', '--elements', type=str, required=True, help='Comma-separated list of column names for the elements (e.g., Transposon, Integron, Insertion_Sequence_Type).')
    parser.add_argument('-g', '--group_column', type=str, required=True, help='Column name for the group (e.g., Country).')

    args = parser.parse_args()

    # 处理元素参数，将逗号分隔的字符串转换为列表
    elements_list = args.elements.split(',')

    # 读取输入文件
    df = pd.read_csv(args.input, sep='\t')

    # 调用主函数
    main(input_file=args.input, output_image=args.output_image, output_table=args.output_table,
         elements=elements_list, group_column=args.group_column)


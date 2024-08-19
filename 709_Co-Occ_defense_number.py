import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: 读取数据
file_path = "All_contigs_info_without_PDC_single_defense.txt"
df = pd.read_csv(file_path, sep='\t')

# Step 2: 数据过滤
filtered_df = df[(df['Defense_Type'].notna()) & (df['Defense_Type'] != 'No')]
filtered_df = filtered_df[(filtered_df['Insertion_Sequence_Type'].notna()) & (filtered_df['Insertion_Sequence_Type'] != 'No')]

# Step 3: 数据分组与计数
grouped_df = filtered_df.groupby(['Defense_Type', 'Sample']).size().reset_index(name='Count')

# Step 4: 绘制Boxplot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Defense_Type', y='Count', data=grouped_df, palette="Set2")
sns.stripplot(x='Defense_Type', y='Count', data=grouped_df, jitter=True, color='black', marker='o', alpha=0.5)

# Step 5: 图形美化
plt.title('Count of Insertion Sequence Types by Defense Type per Sample')
plt.ylabel('Count')
plt.xlabel('Defense Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Step 6: 保存图片
plt.savefig("defense_type_insertion_sequence_boxplot.png", dpi=300)
plt.show()


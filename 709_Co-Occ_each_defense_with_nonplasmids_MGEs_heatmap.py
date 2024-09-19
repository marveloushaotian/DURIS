import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def main(input_file, output_image):
    # Step 1: Read data
    df = pd.read_csv(input_file)

    # Step 2: Data filtering
    filtered_df = df[(df['Defense_Type'].notna()) & (df['Defense_Type'] != 'No')]
    filtered_df = filtered_df[~filtered_df['Defense_Type'].str.startswith(('PDC', 'HEC', 'DMS'))]
    filtered_df = filtered_df[(filtered_df['Insertion_Sequence_Type'].notna()) & (filtered_df['Insertion_Sequence_Type'] != 'No')]

    # Step 3: Split Insertion_Sequence_Type and create new dataframe
    def split_is_types(row):
        is_types = row['Insertion_Sequence_Type'].replace('/', ',').split(',')
        return pd.DataFrame({'Defense_Type': row['Defense_Type'], 'Insertion_Sequence_Type': is_types})

    expanded_df = filtered_df.apply(split_is_types, axis=1).reset_index(drop=True)
    expanded_df = pd.concat(expanded_df.tolist(), ignore_index=True)

    # Step 4: Data grouping and counting
    grouped_df = expanded_df.groupby(['Defense_Type', 'Insertion_Sequence_Type']).size().reset_index(name='Count')

    # Step 5: Create pivot table for heatmap
    pivot_df = grouped_df.pivot(index='Insertion_Sequence_Type', columns='Defense_Type', values='Count').fillna(0)

    # Step 6: Draw Bubble plot
    fig, ax = plt.subplots(figsize=(35, 20))  # Create figure and axis objects
    
    # Define color palette (reversed order)
    colors = ["#e8e7e9", "#e3dce4", "#dcd0dd", "#d5c3d5", "#ceb7ce", "#c6a9c6", "#be9bbc", "#b58db3", "#af82ac", "#aa7aa7", "#a775a4", "#a673a3"]
    cmap = plt.cm.colors.ListedColormap(colors)
    
    # Normalize the data for color mapping
    norm = plt.Normalize(pivot_df.min().min(), pivot_df.max().max())
    
    for i, defense_type in enumerate(pivot_df.columns):
        for j, is_type in enumerate(pivot_df.index):
            size = pivot_df.iloc[j, i]
            color = cmap(norm(size))
            ax.scatter(i, j, s=size*20, c=[color], alpha=0.7)
            ax.text(i, j, f'{size:.0f}', ha='center', va='center', fontweight='bold', fontsize=12)

    # Step 7: Graph beautification
    ax.set_ylabel('Insertion Sequence Type', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(pivot_df.columns)))
    ax.set_xticklabels(pivot_df.columns, rotation=45, ha='right', fontsize=12, fontweight='bold')
    ax.set_yticks(range(len(pivot_df.index)))
    ax.set_yticklabels(pivot_df.index, fontsize=12, fontweight='bold')
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, label='Count')
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label('Count', fontsize=14, fontweight='bold')

    # Step 8: Save image
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze defense types and insertion sequences.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path (CSV format).')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output image file path.')
    args = parser.parse_args()

    main(args.input, args.output)

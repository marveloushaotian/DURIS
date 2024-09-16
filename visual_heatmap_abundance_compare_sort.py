import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate heatmap comparing plasmid and chromosome abundance.')
    parser.add_argument('-c', '--chromosome', required=True, help='Path to chromosome abundance CSV file')
    parser.add_argument('-p', '--plasmid', required=True, help='Path to plasmid abundance CSV file')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output heatmap PDF')
    parser.add_argument('--width', type=int, default=100, help='Width of the output figure (default: 100)')
    parser.add_argument('--height', type=int, default=30, help='Height of the output figure (default: 30)')
    parser.add_argument('--fontsize', type=int, default=15, help='Font size for axis labels (default: 15)')
    return parser.parse_args()

def load_data(file_path):
    data = pd.read_csv(file_path)
    data.set_index('Type', inplace=True)
    return data

def create_custom_colormap():
    return LinearSegmentedColormap.from_list('custom', [
        "#aa7aa7", "#c88b9c", "#d4a29a", "#d6bca7", "#d8d4c1",
        "#cdd2c2", "#c4cfc3", "#beccc5", "#9cb3ad", "#7a9b99",
        "#598287", "#3a6a77"
    ])

def generate_heatmap(chromosome_data, plasmid_data, output_path, figsize, fontsize):
    common_types = chromosome_data.index.intersection(plasmid_data.index)
    chromosome_aligned = chromosome_data.loc[common_types]
    plasmid_aligned = plasmid_data.loc[common_types]

    fold_change = np.log2((plasmid_aligned + 1) / (chromosome_aligned + 1))
    mean_fold_change = fold_change.mean(axis=1)
    sorted_types = mean_fold_change.sort_values().index
    fold_change = fold_change.loc[sorted_types]

    custom_cmap = create_custom_colormap()

    plt.figure(figsize=figsize)
    ax = sns.heatmap(fold_change.T, cmap=custom_cmap, center=0, linewidths=0.1, linecolor='gray',
                     cbar_kws={'label': 'Log2 Fold Change (Plasmid/Chromosome)'})

    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=90, fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()

    plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    args = parse_arguments()

    chromosome_data = load_data(args.chromosome)
    plasmid_data = load_data(args.plasmid)

    generate_heatmap(chromosome_data, plasmid_data, args.output, (args.width, args.height), args.fontsize)

    print(f"Heatmap saved successfully to {args.output}")

if __name__ == "__main__":
    main()
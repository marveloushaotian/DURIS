import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import SymLogNorm, LinearSegmentedColormap
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate heatmaps from abundance data.')
    parser.add_argument('-i', '--input_dir', required=True, help='Input directory containing abundance data files')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory for saving heatmaps')
    parser.add_argument('-m', '--min_nonzero', type=int, default=0, help='Minimum number of non-zero samples to include a type (default: 0)')
    parser.add_argument('--figsize_width', type=int, default=100, help='Width of the figure (default: 100)')
    parser.add_argument('--figsize_height', type=int, default=30, help='Height of the figure (default: 30)')
    parser.add_argument('--fontsize', type=int, default=15, help='Font size for axis labels (default: 15)')
    return parser.parse_args()

def create_custom_colormap():
    return LinearSegmentedColormap.from_list('custom_cmap', [
        '#eaeeea', '#d6ecc1', '#b9df89', '#99ce76',
        '#75b989', '#54a296', '#458689', '#3a6a77'
    ])

def generate_heatmap(file_path, save_path, min_nonzero, figsize, fontsize, custom_cmap):
    data = pd.read_csv(file_path)  # Changed to read CSV
    data.set_index('Type', inplace=True)
    filtered_data = data[(data != 0).sum(axis=1) >= min_nonzero]

    plt.figure(figsize=figsize)
    sns.heatmap(filtered_data.T, cmap=custom_cmap, linewidths=0.1, linecolor='gray', 
                cbar_kws={'label': 'Abundance'},
                norm=SymLogNorm(linthresh=0.03, linscale=0.03, base=10))

    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=90, fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()

    filename = os.path.basename(file_path).replace('.csv', '_heatmap.pdf')  # Changed file extension
    plt.savefig(os.path.join(save_path, filename), format='pdf', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    args = parse_arguments()
    os.makedirs(args.output_dir, exist_ok=True)
    custom_cmap = create_custom_colormap()
    figsize = (args.figsize_width, args.figsize_height)

    for filename in os.listdir(args.input_dir):
        if filename.endswith('.csv'):  # Changed file extension
            file_path = os.path.join(args.input_dir, filename)
            generate_heatmap(file_path, args.output_dir, args.min_nonzero, figsize, args.fontsize, custom_cmap)

    print("Heatmaps generated and saved successfully.")

if __name__ == "__main__":
    main()
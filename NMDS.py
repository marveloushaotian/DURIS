import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.manifold import MDS
from scipy.spatial.distance import pdist, squareform
from skbio import DistanceMatrix
from skbio.stats.distance import anosim

# Function to load data
def load_data(file_path):
    data = pd.read_csv(file_path, sep='\t')
    data.set_index(data.columns[0], inplace=True)
    return data

# Function to perform NMDS and plot with confidence intervals and statistical significance
def plot_nmds(data, group1_cols, group2_cols, title, anosim_p_value, save_path):
    group1 = data[group1_cols]
    group2 = data[group2_cols]
    combined_data = pd.concat([group1, group2], axis=1)

    # Compute the distance matrix
    dist_matrix = squareform(pdist(combined_data.T, metric='braycurtis'))

    # Perform NMDS
    nmds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    nmds_result = nmds.fit_transform(dist_matrix)

    nmds_df = pd.DataFrame(nmds_result, columns=['NMDS1', 'NMDS2'])
    nmds_df['Group'] = ['Before Filter'] * group1.shape[1] + ['After Filter'] * group2.shape[1]

    plt.figure(figsize=(12, 10))
    sns.set(style="whitegrid")

    # Plot NMDS points
    sns.scatterplot(data=nmds_df, x='NMDS1', y='NMDS2', hue='Group', palette=['#F53255', '#00CBBF'], s=100, edgecolor='w', alpha=0.7)

    # Calculate and plot confidence ellipses
    for group, color in zip(['Before Filter', 'After Filter'], ['#F53255', '#00CBBF']):
        subset = nmds_df[nmds_df['Group'] == group]
        mean = np.mean(subset[['NMDS1', 'NMDS2']], axis=0)
        cov = np.cov(subset[['NMDS1', 'NMDS2']], rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        order = eigenvalues.argsort()[::-1]
        eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]

        theta = np.degrees(np.arctan2(*eigenvectors[:, 0][::-1]))
        width, height = 2 * np.sqrt(eigenvalues)

        ellipse = plt.matplotlib.patches.Ellipse(mean, width, height, angle=theta, color=color, alpha=0.2)
        plt.gca().add_patch(ellipse)

    plt.title(f'{title} (ANOSIM p-value: {anosim_p_value:.4f})')
    plt.xlabel('NMDS1')
    plt.ylabel('NMDS2')
    plt.legend(title='Group')
    plt.savefig(os.path.join(save_path, f'{title}.png'))
    plt.close()

# Function to perform ANOSIM analysis
def anosim_analysis(data, group1_cols, group2_cols):
    combined_data = data[group1_cols + group2_cols].T
    grouping = ['Before Filter'] * len(group1_cols) + ['After Filter'] * len(group2_cols)
    distance_matrix = pdist(combined_data, metric='braycurtis')
    distance_matrix = DistanceMatrix(squareform(distance_matrix))
    anosim_result = anosim(distance_matrix, grouping)
    return anosim_result['p-value']

def main(args):
    anova_results = []
    
    for filename in os.listdir(args.directory_path):
        if filename.endswith('.txt') or filename.endswith('.csv'):
            file_path = os.path.join(args.directory_path, filename)
            data = load_data(file_path)
            
            # Print the shape of the data for debugging
            print(f'{filename}: data shape = {data.shape}')
            
            group1_cols = [f'Sample_{i:02d}' for i in range(1, 61)]
            group2_cols = [f'Sample_{i:02d}' for i in range(61, 79)]
            num_columns = data.shape[1]

            # Ensure the column indices are within bounds
            if not all(col in data.columns for col in group1_cols + group2_cols):
                print(f"Error: Specified column indices are out of bounds for {filename}.")
                continue

            # Perform ANOSIM analysis
            anosim_p_value = anosim_analysis(data, group1_cols, group2_cols)

            # Perform NMDS and plot
            plot_nmds(data, group1_cols, group2_cols, filename, anosim_p_value, args.save_path)

            # Store ANOSIM results
            anova_results.append({'Filename': filename, 'ANOSIM p-value': anosim_p_value})

            print(f'{filename}: ANOSIM p-value = {anosim_p_value}')

    # Save ANOSIM results to CSV
    anova_results_df = pd.DataFrame(anova_results)
    anova_results_df.to_csv(args.anova_results_path, index=False)

    # Display ANOSIM results
    print(anova_results_df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform NMDS and ANOSIM on dataset")
    parser.add_argument('-d', '--directory_path', type=str, required=True, help='Directory path containing the data files')
    parser.add_argument('-s', '--save_path', type=str, required=True, help='Path to save the NMDS plots')
    parser.add_argument('-a', '--anova_results_path', type=str, required=True, help='Path to save ANOSIM results CSV')

    args = parser.parse_args()
    main(args)


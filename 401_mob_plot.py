import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from collections import Counter, defaultdict
import logging
from tqdm import tqdm
import numpy as np  # Corrected by adding this line

# Setup logging
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate pie chart for sample types and annotate with Unified Names if applicable.')
    parser.add_argument('-i', '--input', type=str, help='Input filenames, separated by comma: file1.csv,file2.csv')
    parser.add_argument('-o', '--output', type=str, help='Output plot filename (e.g., output.png)')
    args = parser.parse_args()
    return args

def load_data(file1, file2):
    logging.info("Loading data...")
    data1 = pd.read_csv(file1, sep='\t')
    data2 = pd.read_csv(file2, sep=',')
    logging.info("Data loaded successfully.")
    return data1, data2

def preprocess_data(data1, data2):
    logging.info("Preprocessing data...")
    # Extract relevant parts of sample_id for matching
    data1['sample_id_short'] = data1['sample_id'].apply(lambda x: x.split('_NODE')[0])
    logging.info("Data preprocessed successfully.")
    return data1, data2

def plot_data(data1, data2, output_file):
    logging.info("Starting to plot data...")
    sample_types = data1['predicted_mobility'].value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sample_types, autopct='%1.1f%%', textprops=dict(color="w"), colors=plt.cm.viridis(np.linspace(0, 1, 10)))

    # Title for the pie chart
    ax.set_title('Sample Types Distribution')

    # Matching sample_id with seqid in data2
    unified_counts = defaultdict(lambda: defaultdict(int))
    for _, row in tqdm(data1.iterrows(), total=data1.shape[0]):
        sample_type = row['predicted_mobility']
        matches = data2[data2['seqid'] == row['sample_id_short']]['Unified_Name']
        for match in matches:
            unified_counts[sample_type][match] += 1

    # Annotations
    legend_elements = [Patch(facecolor='gray', edgecolor='black',
                             label=f'{sample_type}: ' + ', '.join(f'{key} ({val})' for key, val in names.items()))
                       for sample_type, names in unified_counts.items()]
    ax.legend(handles=legend_elements, title="Unified Names by Sample Type", loc="best", bbox_to_anchor=(1, 0.5))

    # Save the figure
    plt.savefig(output_file, bbox_inches='tight')
    logging.info(f"Plot saved as {output_file}")

def main():
    args = parse_arguments()
    input_files = args.input.split(',')
    data1, data2 = load_data(input_files[0], input_files[1])
    data1, data2 = preprocess_data(data1, data2)
    plot_data(data1, data2, args.output)

if __name__ == "__main__":
    main()


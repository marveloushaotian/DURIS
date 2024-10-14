import pandas as pd
from tqdm import tqdm

def filter_and_split_file(input_file):
    # Read the file
    data = pd.read_csv(input_file, sep="\t")  # Assuming tab-separated
    print(f"Original data shape: {data.shape}")

    # Remove rows where Kaiju_Phylum is 'No'
    filtered_data = data[data['Kaiju_Phylum'] != 'No']
    print(f"Filtered data shape: {filtered_data.shape}")

    # Group by Country and Location_BAF
    grouped = filtered_data.groupby(['Country', 'Location_BAF'])

    # Save each group as a new file
    for (country, location), group in tqdm(grouped, desc="Processing groups"):
        file_name = f"{country}_{location}.txt"
        group.to_csv(file_name, sep="\t", index=False)
        print(f"Saved {file_name}")

# Usage example
input_file = 'all_defense_info_single_full_without_PDC.txt'
filter_and_split_file(input_file)

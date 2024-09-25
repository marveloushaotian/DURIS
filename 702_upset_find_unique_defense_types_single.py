import pandas as pd
import argparse
from tqdm import tqdm

def find_unique_defense_types(input_file, output_file, countries, locations, classifications):
    # 1. Read CSV file
    df = pd.read_csv(input_file)
    
    # 2. Apply filters
    filtered_df = df.copy()
    if countries:
        country_list = countries.split(',')
        filtered_df = filtered_df[filtered_df['Country'].isin(country_list)]
    if locations:
        location_list = locations.split(',')
        filtered_df = filtered_df[filtered_df['Location'].isin(location_list)]
    if classifications:
        classification_list = classifications.split(',')
        filtered_df = filtered_df[filtered_df['Contig_Classification'].isin(classification_list)]

    # 3. Get Defense_Types in filtered data
    filtered_defense_types = filtered_df['Defense_Type'].unique()

    # 4. Count Defense_Types in entire dataset
    defense_type_counts = df['Defense_Type'].value_counts()

    # 5. Find unique Defense_Types
    unique_defense_types = []
    for dt in tqdm(filtered_defense_types, desc="Processing Defense_Types"):
        filtered_count = filtered_df[filtered_df['Defense_Type'] == dt].shape[0]
        total_count = defense_type_counts[dt]
        if filtered_count == total_count:
            dt_countries = df[df['Defense_Type'] == dt]['Country'].unique()
            dt_locations = df[df['Defense_Type'] == dt]['Location'].unique()
            dt_classifications = df[df['Defense_Type'] == dt]['Contig_Classification'].unique()
            if (not countries or set(dt_countries) == set(country_list)) and \
               (not locations or set(dt_locations) == set(location_list)) and \
               (not classifications or set(dt_classifications) == set(classification_list)):
                unique_defense_types.append(dt)

    # 6. Output results
    if not unique_defense_types:
        print("No unique Defense_Type found for the specified conditions.")
    else:
        print("Unique Defense_Type(s) for the specified conditions:")
        for dt in unique_defense_types:
            print(dt)
        
        if output_file:
            result_df = pd.DataFrame({'Unique_Defense_Types': unique_defense_types})
            result_df.to_csv(output_file, index=False)
            print(f"Unique Defense_Type(s) have been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find unique Defense_Type based on specified conditions.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('-c', '--countries', help='Comma-separated list of countries to filter')
    parser.add_argument('-l', '--locations', help='Comma-separated list of Location to filter')
    parser.add_argument('-cc', '--classifications', help='Comma-separated list of Contig_Classification to filter')
    args = parser.parse_args()

    find_unique_defense_types(args.input, args.output, args.countries, args.locations, args.classifications)

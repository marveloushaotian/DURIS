import pandas as pd
import argparse
from itertools import product, chain, combinations
from tqdm import tqdm

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def find_unique_defense_types(input_file, output_file, locations, classifications):
    # 1. Read CSV file
    df = pd.read_csv(input_file)
    
    print("File read successfully. Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("First few rows:")
    print(df.head())
    
    print("Locations:", locations)
    print("Classifications:", classifications)
    
    location_list = locations.split(',') if locations else []
    classification_list = classifications.split(',') if classifications else []
    
    print("Location list:", location_list)
    print("Classification list:", classification_list)
    
    # Check unique values in relevant columns
    print("\nUnique values in 'Location' column:")
    print(df['Location'].unique())
    print("\nUnique values in 'Contig_Classification' column:")
    print(df['Contig_Classification'].unique())
    
    # Check for matching rows
    for loc in location_list:
        for cls in classification_list:
            matching_rows = df[(df['Location'] == loc) & (df['Contig_Classification'] == cls)]
            print(f"\nRows matching Location '{loc}' and Contig_Classification '{cls}': {len(matching_rows)}")
            if not matching_rows.empty:
                print("Sample of matching rows:")
                print(matching_rows[['Location', 'Contig_Classification', 'Defense_Type']].head())
            else:
                print("No matching rows found.")
    
    # 2. Generate all possible single condition combinations
    single_conditions = list(product(location_list, classification_list))
    all_combinations = list(powerset(single_conditions))
    
    print("Sample combinations:")
    for comb in all_combinations[:5]:  # Print first 5 combinations
        print(comb)

    # 3. Create a dictionary to store Defense_Types for each combination
    defense_type_combinations = {comb: set() for comb in all_combinations}

    # 4. Find matching Defense_Types for each combination
    for comb in tqdm(all_combinations, desc="Processing combinations"):
        filtered_df = df
        for loc, cls in comb:
            filtered_df = filtered_df[(filtered_df['Location'] == loc) & 
                                      (filtered_df['Contig_Classification'] == cls)]
        defense_type_combinations[comb] = set(filtered_df['Defense_Type'].unique())
        
        if len(defense_type_combinations[comb]) > 0:
            print(f"Found {len(defense_type_combinations[comb])} defense types for combination {comb}")
        elif len(comb) > 0:
            print(f"No defense types found for combination {comb}")

    # 5. Output Defense_Types for each combination
    print("Defense_Type(s) for different combinations of the specified conditions:")
    for comb, dt_set in defense_type_combinations.items():
        if dt_set:  # Only output non-empty combinations
            print(f"\nCombination: {comb}")
            print("Defense_Types:")
            for dt in dt_set:
                print(f"  - {dt}")
            print("Detailed counts:")
            for dt in dt_set:
                for loc, cls in comb:
                    count = df[(df['Defense_Type'] == dt) & (df['Location'] == loc) & 
                                (df['Contig_Classification'] == cls)].shape[0]
                    if count > 0:
                        print(f"  {dt}: Location: {loc}, Classification: {cls}, Count: {count}")

    # 6. Save results to CSV file if output file is specified
    if output_file:
        result_data = []
        for comb, dt_set in defense_type_combinations.items():
            if dt_set:  # Only save non-empty combinations
                for dt in dt_set:
                    for loc, cls in comb:
                        count = df[(df['Defense_Type'] == dt) & (df['Location'] == loc) & 
                                    (df['Contig_Classification'] == cls)].shape[0]
                        if count > 0:
                            result_data.append({
                                'Combination': str(comb),
                                'Defense_Type': dt,
                                'Location': loc,
                                'Contig_Classification': cls,
                                'Count': count
                            })
        result_df = pd.DataFrame(result_data)
        result_df.to_csv(output_file, index=False)
        print(f"\nDefense_Type(s) for all combinations have been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find Defense_Type for all possible combinations of specified conditions.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('-l', '--locations', help='Comma-separated list of Location to filter')
    parser.add_argument('-cc', '--classifications', help='Comma-separated list of Contig_Classification to filter')
    args = parser.parse_args()

    find_unique_defense_types(args.input, args.output, args.locations, args.classifications)

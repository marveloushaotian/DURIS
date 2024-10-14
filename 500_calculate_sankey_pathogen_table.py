import csv
from collections import defaultdict
import argparse
from tqdm import tqdm

def process_csv(file_path):
    """
    Process CSV file and create a hierarchy structure.
    
    Args:
    file_path (str): Path to the input CSV file
    
    Returns:
    defaultdict: Nested dictionary representing the hierarchy
    """
    hierarchy = defaultdict(lambda: defaultdict(int))
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the header row
        
        for row in tqdm(reader, desc="Processing rows"):
            for i in range(len(row) - 1):
                parent = row[i]
                child = row[i + 1]
                hierarchy[parent][child] += 1
    
    return hierarchy

def print_hierarchy(hierarchy, output_file=None):
    """
    Print or write the hierarchy to a file.
    
    Args:
    hierarchy (defaultdict): Nested dictionary representing the hierarchy
    output_file (str, optional): Path to the output file. If None, print to console.
    """
    output = []
    for parent, children in hierarchy.items():
        for child, count in children.items():
            if count >= 20:  # Only include if count is 10 or more
                output.append(f"{parent} [{count}] {child}")
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write('\n'.join(output))
        print(f"Results written to {output_file}")
    else:
        print('\n'.join(output))

def main():
    parser = argparse.ArgumentParser(description="Process CSV file to create a hierarchy structure.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    args = parser.parse_args()

    hierarchy = process_csv(args.input)
    print_hierarchy(hierarchy, args.output)

if __name__ == "__main__":
    main()
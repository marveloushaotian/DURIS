import pandas as pd
import argparse
import sqlite3
from tqdm import tqdm

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Group and calculate defense statistics by Defense_Type and Kaiju_Phylum.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output CSV file')
args = parser.parse_args()

# Create a temporary SQLite database
print("Creating temporary SQLite database...")
conn = sqlite3.connect(':memory:')

# Read and process data in chunks
print(f"Reading and processing input file: {args.input}")
chunk_size = 100000
for chunk in tqdm(pd.read_csv(args.input, chunksize=chunk_size), desc="Processing chunks"):
    chunk.to_sql('data', conn, if_exists='append', index=False)

# Perform aggregations using SQL
print("Performing aggregations...")
query = """
SELECT 
    Contig_Classification, 
    Sample, 
    Defense_Type, 
    SUM(Defense_Number) as Defense_Number,
    SUM(Contig_Length) as Contig_Length,
    MAX(Location) as Location,
    MAX(Country) as Country,
    MAX(Season) as Season,
    SUM(Defense_Number) * 1000000.0 / SUM(Contig_Length) as GCGB
FROM data
GROUP BY Contig_Classification, Sample, Defense_Type
"""
grouped = pd.read_sql_query(query, conn)

# Count Kaiju_Phylum occurrences
print("Counting Kaiju_Phylum occurrences...")
phylum_query = """
SELECT 
    Contig_Classification, 
    Sample, 
    Defense_Type, 
    Kaiju_Phylum,
    COUNT(*) as Count
FROM data
WHERE Kaiju_Phylum != 'No'
GROUP BY Contig_Classification, Sample, Defense_Type, Kaiju_Phylum
"""
phylum_counts = pd.read_sql_query(phylum_query, conn)

# Pivot the phylum counts
phylum_counts_pivot = phylum_counts.pivot_table(
    values='Count', 
    index=['Contig_Classification', 'Sample', 'Defense_Type'],
    columns='Kaiju_Phylum', 
    fill_value=0
)

# Merge the grouped data with phylum counts
result = pd.merge(grouped, phylum_counts_pivot, on=['Contig_Classification', 'Sample', 'Defense_Type'], how='left')

# Fill NaN values with 0 for phylum counts
result = result.fillna(0)

# Export the result
print(f"Exporting results to: {args.output}")
result.to_csv(args.output, index=False)

print(f"Results have been exported to {args.output}")

# Close the database connection
conn.close()

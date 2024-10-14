import pandas as pd

# Read all files
contigs = pd.read_csv('all_contigs_kaiju_taxa_name_kingdom_processed.txt', sep='\t')
phylum = pd.read_csv('all_contigs_kaiju_taxa_name_phylum_processed.txt', sep='\t')
class_ = pd.read_csv('all_contigs_kaiju_taxa_name_class_processed.txt', sep='\t')
order = pd.read_csv('all_contigs_kaiju_taxa_name_order_processed.txt', sep='\t')
family = pd.read_csv('all_contigs_kaiju_taxa_name_family_processed.txt', sep='\t')
genus = pd.read_csv('all_contigs_kaiju_taxa_name_genus_processed.txt', sep='\t')
species = pd.read_csv('all_contigs_kaiju_taxa_name_species_processed.txt', sep='\t')

# Merge all files
merged_df = contigs.merge(phylum, on='Contig_ID', how='outer', suffixes=('', '_phylum')) \
                   .merge(class_, on='Contig_ID', how='outer', suffixes=('', '_class')) \
                   .merge(order, on='Contig_ID', how='outer', suffixes=('', '_order')) \
                   .merge(family, on='Contig_ID', how='outer', suffixes=('', '_family')) \
                   .merge(genus, on='Contig_ID', how='outer', suffixes=('', '_genus')) \
                   .merge(species, on='Contig_ID', how='outer', suffixes=('', '_species'))

# Save the result to a new file
merged_df.to_csv('all_contigs_kaiju_taxa_merged.txt', sep='\t', index=False)

print("Files have been successfully merged and saved to 'all_contigs_kaiju_taxa_merged.txt'.")

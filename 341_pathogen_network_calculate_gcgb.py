import os
import pandas as pd
import argparse
from tqdm import tqdm

# List of pathogenic species
pathogenic_species = [
    "Achromobacter_denitrificans", "Achromobacter_ruhlandii", "Achromobacter_xylosoxidans",
    "Acinetobacter_baumannii", "Acinetobacter_calcoaceticus", "Acinetobacter_Iwoffii",
    "Acinetobacter_johnsonii", "Acinetobacter_pittii", "Actinomyces_israelii", "Actinomyces_naeslundii",
    "Actinomyces_viscosus", "Actinomycetes", "Aeromonas_caviae", "Aeromonas_hydrophila", "Aeromonas_media",
    "Aeromonas_schubertii", "Aeromonas_sobria", "Aeromonas_veronii", "Alcaligenes_faecalis",
    "Alcaligenes_xylosoxidans", "Bacillus_anthracis", "Bacillus_cereus", "Bacillus_subtilis",
    "Bacteroides_fragilis", "Bartonella_quintana", "Bordetella_pertussis", "Borrelia_burgdorferi",
    "Borrelia_duttoni", "Borrelia_recurrentis", "Brevundimonas_diminuta", "Brevundimonas_vesicularis",
    "Brucella_abortus", "Brucella_canis", "Brucella_melitensis", "Brucella_suis", "Burkholderia_cepacia",
    "Burkholderia_mallei", "Burkholderia_pseudomallei", "Campylobacter_jejuni", "Chlamydia_pneumoniae",
    "Chlamydia_psittaci", "Chlamydia_trachomatis", "Citrobacter_braakii", "Citrobacter_freundii",
    "Citrobacter_koseri", "Clostridioides_difficile", "Clostridium_botulinum", "Clostridium_perfringens",
    "Clostridium_tetani", "Corynebacterium_diphtheriae", "Corynebacterium_jeikeium",
    "Corynebacterium_pseudotuberculosis", "Corynebacterium_ulcerans", "Corynebacterium_urealyticum",
    "Coxiella_burnetii", "Dermatophilus_congolensis", "Enterobacter_aerogenes", "Enterobacter_cloacae",
    "Enterococcus_faecalis", "Enterococcus_faecium", "Enterococcus_hirae", "Escherichia_coli",
    "Francisella_tularensis", "Gordonia_bronchialis", "Haemophilus_influenzae", "Helicobacter_pylori",
    "Klebsiella_granulomatis", "Klebsiella_oxytoca", "Klebsiella_pneumoniae", "Leclercia_adecarboxylata",
    "Legionella_pneumophila", "Leptospira_interrogans", "Leuconostoc_pseudomesenteroides",
    "Listeria_monocytogenes", "Micrococcus_luteus", "Moraxella_catarrhalis", "Morganella_morganii",
    "Mycobacterium_basiliense", "Mycobacterium_chimaera", "Mycobacterium_leprae", "Mycobacterium_tuberculosis",
    "Mycoplasma_genitalium", "Mycoplasma_pneumoniae", "Neisseria_gonorrhoeae", "Neisseria_meningitidis",
    "Nocardia_asteroides", "Nocardia_brasiliensis", "Orientia_tsutsugamushi", "Pantoea_agglomerans",
    "Paracoccus_yeei", "Prevotella_bivia", "Prevotella_corporis", "Prevotella_intermedia",
    "Prevotella_melaninogenica", "Propionibacterium_species", "Proteus_mirabilis", "Proteus_vulgaris",
    "Providencia_rettgeri", "Providencia_stuartii", "Pseudomonas_aeruginosa", "Pseudomonas_fluorescens",
    "Pseudomonas_putida", "Ralstonia_mannitolilytica", "Ralstonia_pickettii", "Rhodococcus_equi",
    "Rickettsia_prowazekii", "Rickettsia_typhi", "Roseomonas_gilardii", "Salmonella_enterica",
    "Salmonella_Enteritidis", "Salmonella_Paratyphi", "Salmonella_Typhi", "Salmonella_Typhimurium",
    "Serratia_marcescens", "Shigella_sonnei", "Sphingomonas_species", "Staphylococcus_aureus",
    "Staphylococcus_capitis", "Staphylococcus_epidermidis", "Staphylococcus_haemolyticus",
    "Staphylococcus_hominis", "Staphylococcus_lugdunensis", "Staphylococcus_pasteuri",
    "Staphylococcus_saprophyticus", "Stenotrophomonas_maltophilia", "Streptococcus_agalactiae",
    "Streptococcus_mutans", "Streptococcus_pneumoniae", "Streptococcus_pyogenes", "Streptococcus_viridans",
    "Streptomyces_griseus", "Streptomyces_somaliensis", "Treponema_pallidum", "Tsukamurella_paurometabola",
    "Vibrio_cholerae", "Yersinia_enterocolitica", "Yersinia_pestis", "Yersinia_pseudotuberculosis"
]

def compute_defense_statistics(input_file, output_file, filter_pathogens=False, reference_file=None):
    # 1. Read the input CSV file
    df = pd.read_csv(input_file)

    # 2. Filter rows based on Kaiju_Species if filter_pathogens is True
    if filter_pathogens:
        df = df[df['Kaiju_Species'].isin(pathogenic_species)]

    # 3. Group by 'Kaiju_Species' and 'Defense_Type', and calculate the count
    grouped = df.groupby(['Kaiju_Species', 'Defense_Type']).size().reset_index(name='Count')

    # 4. If reference_file is provided, match and merge additional columns
    if reference_file:
        ref_df = pd.read_csv(reference_file)
        # Extract Location, Country, and Contig_Classification from the input file name
        file_parts = os.path.basename(input_file).split('_')
        location, country = file_parts[:2]
        country = country.split('.')[0]  # Remove file extension
        contig_classification = '_'.join(file_parts[2:]).split('.')[0]  # Join remaining parts and remove extension
        
        # Filter reference dataframe based on Location, Country, and Contig_Classification
        ref_df_filtered = ref_df[(ref_df['Location'] == location) & 
                                 (ref_df['Country'] == country) & 
                                 (ref_df['Contig_Classification'] == contig_classification)]
        
        # Merge on 'Defense_Type'
        merged_df = pd.merge(grouped, ref_df_filtered[['Defense_Type', 'Total_Defense_Num', 'Total_Contig_Length', 'GCGB']], 
                             on='Defense_Type', how='left')
        
        # Select only the required columns
        grouped = merged_df[['Kaiju_Species', 'Defense_Type', 'Count', 'Total_Defense_Num', 'Total_Contig_Length', 'GCGB']]

    # 5. Save the results to a new CSV file
    grouped.to_csv(output_file, index=False)

def process_directory(input_dir, output_dir, filter_pathogens=False, reference_file=None):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get a list of all CSV files in the input directory
    for filename in tqdm(os.listdir(input_dir), desc="Processing files"):
        if filename.endswith(".csv"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)
            
            # Compute defense statistics for each file
            compute_defense_statistics(input_file_path, output_file_path, filter_pathogens, reference_file)
            print(f"Processed file saved: {output_file_path}")

def main():
    # 6. Set up argument parser
    parser = argparse.ArgumentParser(description="Compute statistics for Kaiju_Species and Defense_Type for all CSV files in a directory, and save to a new directory")
    parser.add_argument('-i', '--input_dir', type=str, required=True, help="Directory containing the input CSV files")
    parser.add_argument('-o', '--output_dir', type=str, required=True, help="Directory to save the output CSV files")
    parser.add_argument('-f', '--filter_pathogens', action='store_true', help="Filter rows to include only pathogenic species")
    parser.add_argument('-r', '--reference_file', type=str, help="Reference CSV file to match and merge additional columns")
    args = parser.parse_args()

    # 7. Process the directory
    process_directory(args.input_dir, args.output_dir, args.filter_pathogens, args.reference_file)

if __name__ == "__main__":
    main()

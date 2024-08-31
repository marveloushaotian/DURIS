#!/bin/bash

# conda activate prodigal

run_prodigal() {
    local input=$1
    local output_dir=$2
    local name=$(basename "$input" .fasta)
    
    mkdir -p "Source/03_genes/$output_dir"/{logs,gff,fna,faa}
    
    prodigal -i "$input" -f gff \
             -o "Source/03_genes/$output_dir/gff/${name}.gff3" \
             -d "Source/03_genes/$output_dir/fna/${name}.fna" \
             -a "Source/03_genes/$output_dir/faa/${name}.faa" \
             -p meta &> "Source/03_genes/$output_dir/logs/${name}.log"
}

export -f run_prodigal

echo "Starting gene and protein prediction based on nucleotide files..."

# Define datasets to process
datasets=(
    "Source/02_contigs/02_plasmid/final_metagenome_plasmid_circular_plaspline_split/* 02_plasmid/metagenome_plasmid_circular_plaspline"
    "Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_genomad_split/* 02_plasmid/metagenome_plasmid_linear_genomad"
    "Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_plaspline_split/* 02_plasmid/metagenome_plasmid_linear_plaspline"
    "Source/02_contigs/02_plasmid/final_plasmidome_plasmid_circular_plaspline_split/* 02_plasmid/plasmidome_plasmid_circular_plaspline"
    "Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_genomad_split/* 02_plasmid/plasmidome_plasmid_linear_genomad"
    "Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_plaspline_split/* 02_plasmid/plasmidome_plasmid_linear_plaspline"
    "Source/02_contigs/04_phage/final_metagenome_phage_split/* 04_phage/metagenome_phage"
    "Source/02_contigs/04_phage/final_plasmidome_phage_split/* 04_phage/plasmidome_phage"
    "Source/02_contigs/03_chromosome/metagenome_chromosome_split_largechunk/* 03_chromosome/metagenome_chromosome_large_chunk"
    "Source/02_contigs/03_chromosome/plasmidome_chromosome_split/* 03_chromosome/plasmidome_chromosome"
)

for dataset in "${datasets[@]}"; do
    read -r input_path output_dir <<< "$dataset"
    echo "Processing: $output_dir"
    parallel -j40 run_prodigal ::: $input_path ::: "$output_dir"
done

echo "All gene predictions are complete."
#!/bin/bash

# conda activate prodigal

doit(){
    mkdir -p Source/03_genes/${2}/logs
    NAME=$(echo $1 | sed 's|.*\/||;s|\.fasta||')
    mkdir -p Source/03_genes/${2}/gff
    mkdir -p Source/03_genes/${2}/fna
    mkdir -p Source/03_genes/${2}/faa
    prodigal -i ${1} -f gff -o Source/03_genes/${2}/gff/${NAME}.gff3 -d Source/03_genes/${2}/fna/${NAME}.fna -a Source/03_genes/${2}/faa/${NAME}.faa -p meta &> Source/03_genes/${2}/logs/${NAME}.log
}

export -f doit

echo "Starting predict gene and proteins based on nucleotide file..."

# echo "contig: metagenome plasmid circular plaspline"
# parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_circular_plaspline_split/* ::: 02_plasmid/metagenome_plasmid_circular_plaspline

# echo "contig: metagenome plasmid linear genomad"
# parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_genomad_split/* ::: 02_plasmid/metagenome_plasmid_linear_genomad

# echo "contig: metagenome plasmid linear plaspline"
# parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_plaspline_split/* ::: 02_plasmid/metagenome_plasmid_linear_plaspline

# echo "contig: plasmidome plasmid circular plaspline"
# parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_circular_plaspline_split/* ::: 02_plasmid/plasmidome_plasmid_circular_plaspline

# echo "contig: plasmidome plasmid linear genomad"
# parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_genomad_split/* ::: 02_plasmid/plasmidome_plasmid_linear_genomad

# echo "contig: plasmidome plasmid linear plaspline"
# parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_plaspline_split/* ::: 02_plasmid/plasmidome_plasmid_linear_plaspline

# echo "contig: metagenome phage"
# parallel -j40 doit ::: Source/02_contigs/04_phage/final_metagenome_phage_split/* ::: 04_phage/metagenome_phage

# echo "contig: plasmidome phage"
# parallel -j40 doit ::: Source/02_contigs/04_phage/final_plasmidome_phage_split/* ::: 04_phage/plasmidome_phage

echo "contig: metagenome chromosome large chunk"

parallel -j40 doit ::: Source/02_contigs/03_chromosome/metagenome_chromosome_split_largechunk/* ::: 03_chromosome/metagenome_chromosome_large_chunk

# echo "contig: plasmidome chromosome"

# parallel -j40 doit ::: Source/02_contigs/03_chromosome/plasmidome_chromosome_split/* ::: 03_chromosome/plasmidome_chromosome

echo "All gene prediction are complete."

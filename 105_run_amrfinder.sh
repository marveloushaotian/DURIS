#!/bin/bash

# conda activate amrfinder

doit(){
    mkdir -p Process/02.ARGs/01_AMRFinder/${2}/logs
    NAME=$(echo $1 | sed 's|.*\/||;s|\.fasta||')
    mkdir -p Process/02.ARGs/01_AMRFinder/${2}
    amrfinder --plus -n Source/02_contigs/${1} -o Process/02.ARGs/01_AMRFinder/${2}/${NAME}_amrfinder.txt &> Process/02.ARGs/01_AMRFinder/${2}/logs/${NAME}.log
}d

export -f doit

echo "Starting amr gene annotation with AMRFINDER for all contigs..."

echo "contig: metagenome plasmid circular plaspline"
parallel -j40 doit ::: 02_plasmid/final_metagenome_plasmid_circular_plaspline_split/* ::: metagenome_plasmid_circular_plaspline

echo "contig: metagenome plasmid linear genomad"
parallel -j40 doit ::: 02_plasmid/final_metagenome_plasmid_linear_genomad_split/* ::: metagenome_plasmid_linear_genomad

echo "contig: metagenome plasmid linear plaspline"
parallel -j40 doit ::: 02_plasmid/final_metagenome_plasmid_linear_plaspline_split/* ::: metagenome_plasmid_linear_plaspline

echo "contig: plasmidome plasmid circular plaspline"
parallel -j40 doit ::: 02_plasmid/final_plasmidome_plasmid_circular_plaspline_split/* ::: plasmidome_plasmid_circular_plaspline

echo "contig: plasmidome plasmid linear genomad"
parallel -j40 doit ::: 02_plasmid/final_plasmidome_plasmid_linear_genomad_split/* ::: plasmidome_plasmid_linear_genomad

echo "contig: plasmidome plasmid linear plaspline"
parallel -j40 doit ::: 02_plasmid/final_plasmidome_plasmid_linear_plaspline_split/* ::: plasmidome_plasmid_linear_plaspline

echo "contig: metagenome phage"
parallel -j40 doit ::: 04_phage/final_metagenome_phage_split/* ::: metagenome_phage

echo "contig: plasmidome phage"
parallel -j40 doit ::: 04_phage/final_plasmidome_phage_split/* ::: plasmidome_phage

echo "contig: metagenome chromosome"

parallel -j40 doit ::: 03_chromosome/metagenome_chromosome_split_largechunk/* ::: metagenome_chromosome

echo "contig: plasmidome chromosome"

parallel -j40 doit ::: 03_chromosome/plasmidome_chromosome_split_largechunk/* ::: plasmidome_chromosome

echo "All amr gene annotation are complete."

#!/bin/bash

# conda activate integronfinder

doit(){
    mkdir -p Process/03.Non_plasmids_MGEs/01.Integron/${2}/logs
    NAME=$(echo $1 | sed 's|.*\/||;s|\.fasta||')
    mkdir -p Process/03.Non_plasmids_MGEs/01.Integron${2}/
    integron_finder --local-max --func-annot ${1} --outdir Process/03.Non_plasmids_MGEs/01.Integron${2}/ &> Process/03.Non_plasmids_MGEs/01.Integron${2}/logs/${NAME}.log
}

export -f doit

echo "Starting integron annotation with INTEGRONFINDER for contigs..."

echo "contig: metagenome plasmid circular plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_circular_plaspline_split/* ::: metagenome_plasmid_circular_plaspline

echo "contig: metagenome plasmid linear genomad"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_genomad_split/* ::: metagenome_plasmid_linear_genomad

echo "contig: metagenome plasmid linear plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_plaspline_split/* ::: metagenome_plasmid_linear_plaspline

echo "contig: plasmidome plasmid circular plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_circular_plaspline_split/* ::: plasmidome_plasmid_circular_plaspline

echo "contig: plasmidome plasmid linear genomad"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_genomad_split/* ::: plasmidome_plasmid_linear_genomad

echo "contig: plasmidome plasmid linear plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_plaspline_split/* ::: plasmidome_plasmid_linear_plaspline

echo "contig: metagenome phage"
parallel -j40 doit ::: Source/02_contigs/04_phage/final_metagenome_phage_split/* ::: metagenome_phage

echo "contig: plasmidome phage"
parallel -j40 doit ::: Source/02_contigs/04_phage/final_plasmidome_phage_split/* ::: plasmidome_phage

echo "contig: metagenome chromosome"

parallel -j40 doit ::: Source/02_contigs/03_chromosome/metagenome_chromosome_split/* ::: metagenome_chromosome

echo "contig: plasmidome chromosome"

parallel -j40 doit ::: Source/02_contigs/03_chromosome/plasmidome_chromosome_split/* ::: plasmidome_chromosome

echo "All defense systems annotation are complete."

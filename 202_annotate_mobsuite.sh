#!/bin/bash

# conda activate mobsuite

doit() {
    mkdir -p Process/05.Plasmids_features/01.MOB_suite/${2}/logs
    NAME=$(echo $1 | sed 's|.*\/||;s|\.fasta||')
    mkdir -p Process/05.Plasmids_features/01.MOB_suite/${2}/${NAME}
    mob_typer --multi --infile ${1} --out_file Process/05.Plasmids_features/01.MOB_suite/${2}/${NAME}_mobsuite.txt &> Process/05.Plasmids_features/01.MOB_suite/${2}/logs/${NAME}.log
}

export -f doit

echo "Starting plasmids features annotation for plasmids contigs..."

echo "contig: metagenome plasmid circular plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_circular_plaspline_split/* ::: metagenome_plasmid_circular_plaspline

echo "contig: metagenome plasmid linear genomad"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_genomad_split/* ::: metagenome_plasmid_linear_genomad

echo "contig: metagenome plasmid linear plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_plaspline_split/* ::: final_metagenome_plasmid_linear_plaspline

echo "contig: plasmidome plasmid circular plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_circular_plaspline_split/* ::: final_plasmidome_plasmid_circular_plaspline

echo "contig: plasmidome plasmid linear genomad"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_genomad_split/* ::: final_plasmidome_plasmid_linear_genomad

echo "contig: plasmidome plasmid linear plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_plaspline_split/* ::: final_plasmidome_plasmid_linear_plaspline

echo "All plasmids features annotation are complete."

#!/bin/bash

# conda activate bacant

doit(){
    mkdir -p ${2}/logs
    NAME=$(echo $1 | sed 's|.*\/||;s|\.fasta||')
    mkdir -p ${2}/${NAME}
    bacant -n ${1} -o ${2}/${NAME} &> ${2}/logs/${NAME}.log
}

export -f doit
echo "metagenome_chromosome"
parallel -j40 doit ::: Source/02_contigs/03_chromosome/metagenome_chromosome_split_largechunk/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/metagenome_chromosome
echo "plasmidome_chromosome"
parallel -j40 doit ::: Source/02_contigs/03_chromosome/plasmidome_chromosome_split_largechunk/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/plasmidome_chromosome
echo "final_metagenome_plasmid_circular_plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_circular_plaspline_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_metagenome_plasmid_circular_plaspline
echo "final_metagenome_plasmid_linear_genomad"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_genomad_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_metagenome_plasmid_linear_genomad
echo "final_metagenome_plasmid_linear_plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_metagenome_plasmid_linear_plaspline_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_metagenome_plasmid_linear_plaspline
echo "final_plasmidome_plasmid_circular_plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_circular_plaspline_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_plasmidome_plasmid_circular_plaspline
echo "final_plasmidome_plasmid_linear_genomad"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_genomad_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_plasmidome_plasmid_linear_genomad
echo "final_plasmidome_plasmid_linear_plaspline"
parallel -j40 doit ::: Source/02_contigs/02_plasmid/final_plasmidome_plasmid_linear_plaspline_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_plasmidome_plasmid_linear_plaspline
echo "final_metagenome_phage"
parallel -j40 doit ::: Source/02_contigs/04_phage/final_metagenome_phage_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_metagenome_phage
echo "final_plasmidome_phage"
parallel -j40 doit ::: Source/02_contigs/04_phage/final_plasmidome_phage_split/* ::: Process/03.Non_plasmids_MGEs/03.Transposon/final_plasmidome_phage

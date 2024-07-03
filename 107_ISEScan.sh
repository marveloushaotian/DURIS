#!/bin/bash

# conda activate ISEScan

doit(){
    mkdir -p Process/03.Non_plasmids_MGEs/02.IS/01.ISEScan/${2}/logs
    NAME=$(echo $1 | sed 's|.*\/||;s|\.fna||')
    mkdir -p Process/03.Non_plasmids_MGEs/02.IS/01.ISEScan/${2}
    isescan.py --seqfile ${1} --output Process/03.Non_plasmids_MGEs/02.IS/01.ISEScan/${2} &> Process/03.Non_plasmids_MGEs/02.IS/01.ISEScan/${2}/logs/${NAME}.log
}

export -f doit

echo "Starting IS annotation with ISEScan for plasmids contigs..."

echo "contig: metagenome plasmid circular plaspline"
parallel -j80 doit ::: Source/03_genes/02_plasmid/metagenome_plasmid_circular_plaspline/fna/* ::: metagenome_plasmid_circular_plaspline

echo "contig: metagenome plasmid linear genomad"
parallel -j80 doit ::: Source/03_genes/02_plasmid/metagenome_plasmid_linear_genomad/fna/* ::: metagenome_plasmid_linear_genomad

echo "contig: metagenome plasmid linear plaspline"
parallel -j80 doit ::: Source/03_genes/02_plasmid/metagenome_plasmid_linear_plaspline/fna/* ::: metagenome_plasmid_linear_plaspline

echo "contig: plasmidome plasmid circular plaspline"
parallel -j80 doit ::: Source/03_genes/02_plasmid/plasmidome_plasmid_circular_plaspline/fna/* ::: plasmidome_plasmid_circular_plaspline

echo "contig: plasmidome plasmid linear genomad"
parallel -j80 doit ::: Source/03_genes/02_plasmid/plasmidome_plasmid_linear_genomad/fna/* ::: plasmidome_plasmid_linear_genomad

echo "contig: plasmidome plasmid linear plaspline"
parallel -j80 doit ::: Source/03_genes/02_plasmid/plasmidome_plasmid_linear_plaspline/fna/* ::: plasmidome_plasmid_linear_plaspline

echo "contig: metagenome phage"
parallel -j80 doit ::: Source/03_genes/04_phage/metagenome_phage/fna/* ::: metagenome_phage

echo "contig: plasmidome phage"
parallel -j80 doit ::: Source/03_genes/04_phage/plasmidome_phage/fna/* ::: plasmidome_phage

echo "contig: metagenome chromosome"

parallel -j80 doit ::: Source/03_genes/03_chromosome/metagenome_chromosome/fna/* ::: metagenome_chromosome

echo "contig: plasmidome chromosome"

parallel -j80 doit ::: Source/03_genes/03_chromosome/plasmidome_chromosome/fna/* ::: plasmidome_chromosome

echo "All IS annotation are complete."

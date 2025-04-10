#!/bin/bash

# conda activate defensefinder

doit(){
    mkdir -p Process/03.Defense/02.DefenseFinder/${2}/logs
    mkdir -p Process/03.Defense/02.DefenseFinder/${2}/idx
    NAME=$(echo $1 | sed 's|.*\/||;s|\.faa||')
    mkdir -p Process/03.Defense/02.DefenseFinder/${2}
    defense-finder run ${1} -o Process/03.Defense/02.DefenseFinder/${2}/${NAME} --db-type unordered --models-dir /home/projects/ku_00041/data/PEACE/Haotian/Software/Anaconda3/envs/defensefinder/share/macsyfinder/data/models &> Process/03.Defense/02.DefenseFinder/${2}/logs/${NAME}.log
    mv Process/03.Defense/01.PADLOC/plasmid/${3}/${NAME}.faa.idx Process/03.Defense/02.DefenseFinder/${2}/idx
}

export -f doit

echo "Starting defense annotation with Defense Finder for plasmids contigs..."

echo "contig: metagenome_plasmid_circular_plaspline"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/plasmid/metagenome_plasmid_circular_plaspline/*.faa ::: metagenome_plasmid_circular_plaspline ::: metagenome_plasmid_circular_plaspline

echo "contig: metagenome_plasmid_linear_genomad"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/plasmid/metagenome_plasmid_linear_genomad/*.faa ::: metagenome_plasmid_linear_genomad ::: metagenome_plasmid_linear_genomad

echo "contig: metagenome_plasmid_linear_plaspline"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/plasmid/metagenome_plasmid_linear_plaspline/*.faa ::: metagenome_plasmid_linear_plaspline ::: metagenome_plasmid_linear_plaspline

echo "contig: plasmidome_plasmid_circular_plaspline"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/plasmid/plasmidome_plasmid_circular_plaspline/*.faa ::: plasmidome_plasmid_circular_plaspline ::: plasmidome_plasmid_circular_plaspline

echo "contig: plasmidome_plasmid_linear_genomad"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/plasmid/plasmidome_plasmid_linear_genomad/*.faa ::: plasmidome_plasmid_linear_genomad ::: plasmidome_plasmid_linear_genomad

echo "contig: plasmidome_plasmid_linear_plaspline"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/plasmid/plasmidome_plasmid_linear_plaspline/*.faa ::: plasmidome_plasmid_linear_plaspline ::: plasmidome_plasmid_linear_plaspline

echo "contig: Metagenome Phage"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/phage/metagenome_phage/*.faa ::: Metagenome_Phage ::: Metagenome_Phage

echo "contig: Plasmidome Phage"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/phage/plasmidome_phage/*.faa ::: Plasmidome_Phage ::: Plasmidome_Phage

echo "contig: Metagenome Chromosome"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/chromosome/metagenome_chromosome/*.faa ::: Metagenome_Chromosome ::: Metagenome_Chromosome

echo "contig: Plasmidome Chromosome, but actually is plasmid"
parallel -j12 doit ::: Process/03.Defense/01.PADLOC/chromosome/plasmidome_chromosome/*.faa ::: Plasmidome_Chromosome ::: Plasmidome_Chromosome

echo "All defense systems annotation are complete."


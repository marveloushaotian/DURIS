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

echo "contig: chromosome"
parallel -j12 doit ::: Source/02_contigs/03_chromosome/fastas/chromosome.fasta ::: chromosome ::: chromosome

echo "contig: plasmid"
parallel -j12 doit ::: Source/02_contigs/02_plasmid/fastas/plasmid.fasta ::: plasmid ::: plasmid

echo "contig: phage"
parallel -j12 doit ::: Source/02_contigs/04_phage/fastas/phage.fasta ::: phage ::: phage

echo "All defense systems annotation are complete."


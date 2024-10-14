#!/bin/bash

# conda activate eggnog

doit(){
    NAME=$(echo $1 | sed 's|.*\/||;s|\.faa||')
    mkdir 10 -p Process/04.Function/01.COG/metagenome_chromosome
    emapper.py --cpu 10 -m mmseqs --no_annot --no_file_comments -i ${1} -o Process/04.Function/01.COG/metagenome_chromosome/${2}_${NAME}
}

export -f doit

echo "Starting eggnog annotation with EGGNOG for contigs..."

# echo "contig: metagenome plasmid circular plaspline"
# parallel -j40 doit ::: Source/03_genes/02_plasmid/metagenome_plasmid_circular_plaspline/meta_ps_cr_pl.faa ::: meta_ps_cr_pl

# echo "contig: metagenome plasmid linear genomad"
# parallel -j40 doit ::: Source/03_genes/02_plasmid/metagenome_plasmid_linear_genomad/meta_ps_ln_ge.faa ::: meta_ps_ln_ge

# echo "contig: metagenome plasmid linear plaspline"
# parallel -j40 doit ::: Source/03_genes/02_plasmid/metagenome_plasmid_linear_plaspline/meta_ps_ln_pl.faa ::: meta_ps_ln_pl

# echo "contig: plasmidome plasmid circular plaspline"
# parallel -j40 doit ::: Source/03_genes/02_plasmid/plasmidome_plasmid_circular_plaspline/plas_ps_cr_pl.faa ::: plas_ps_cr_pl

# echo "contig: plasmidome plasmid linear genomad"
# parallel -j40 doit ::: Source/03_genes/02_plasmid/plasmidome_plasmid_linear_genomad/plas_ps_ln_ge.faa ::: plas_ps_ln_ge

# echo "contig: plasmidome plasmid linear plaspline"
# parallel -j40 doit ::: Source/03_genes/02_plasmid/plasmidome_plasmid_linear_plaspline/plas_ps_ln_pl.faa ::: plas_ps_ln_ge

# echo "contig: metagenome phage"
# parallel -j40 doit ::: Source/03_genes/04_phage/metagenome_phage/meta_ph.faa ::: meta_ph

# echo "contig: plasmidome phage"
# parallel -j40 doit ::: Source/03_genes/04_phage/plasmidome_phage/plas_ph.faa ::: plas_ph

echo "contig: metagenome chromosome"

parallel -j2 doit ::: Source/03_genes/03_chromosome/metagenome_chromosome_large_chunk/faa/* ::: meta_cm

# echo "contig: plasmidome chromosome"

# parallel -j40 doit ::: Source/03_genes/03_chromosome/plasmidome_chromosome/plas_cm.faa ::: plas_cm

echo "All cog annotation are complete."

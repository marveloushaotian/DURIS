#!/bin/bash

# conda activate padloc

doit() {
    INPUT="$1"        # Input .fasta file
    TYPE="$2"         # Contig type: chromosome / plasmid / phage

    NAME=$(basename "$INPUT" | sed 's/\.fasta\(\.gz\)\{0,1\}$//')
    OUTDIR=Process/03.Defense/01.PADLOC/${TYPE}
    LOGDIR=${OUTDIR}/logs
    RESULTDIR=${OUTDIR}/results/${NAME}

    # Create all required directories
    mkdir -p "$OUTDIR" "$LOGDIR" "${OUTDIR}/results"

    echo "[$(date)] Running PADLOC on $NAME..." | tee -a "$LOGDIR/${NAME}.log"

    # Remove existing result directory if present
    if [ -d "$RESULTDIR" ]; then
        echo "[$(date)] Output directory $RESULTDIR already exists. Deleting..." >> "$LOGDIR/${NAME}.log"
        rm -rf "$RESULTDIR"
    fi

    # Create the result directory explicitly before running PADLOC
    mkdir -p "$RESULTDIR"

    # Run PADLOC
    padloc --fna "$INPUT" \
           --outdir "$RESULTDIR" \
           --fix-prodigal \
           &>> "$LOGDIR/${NAME}.log"

    if [ $? -ne 0 ]; then
        echo "[$(date)] ERROR: PADLOC failed for $NAME" >> "$LOGDIR/${NAME}.log"
        return 1
    else
        echo "[$(date)] PADLOC completed successfully for $NAME" >> "$LOGDIR/${NAME}.log"
        return 0
    fi
}

export -f doit

echo "[$(date)] Starting PADLOC batch annotation..."

# chromosome
echo "Contig type: chromosome"
parallel -j40 doit ::: Source/03_genes/03_chromosome/split_chromosome/*.fasta ::: chromosome

# plasmid
echo "Contig type: plasmid"
parallel -j40 doit ::: Source/03_genes/02_plasmid/split_plasmid/*.fasta ::: plasmid

# phage
echo "Contig type: phage"
parallel -j40 doit ::: Source/03_genes/04_phage/split_phage/*.fasta ::: phage

echo "[$(date)] All PADLOC annotations completed."

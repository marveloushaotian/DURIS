#!/bin/bash

doit() {
    INPUT="$1"
    TYPE="$2"

    NAME=$(basename "$INPUT" | sed 's/\.faa\(\.gz\)\{0,1\}$//')
    OUTDIR=Process/03.Defense/02.DefenseFinder/${TYPE}
    LOGDIR=${OUTDIR}/logs
    IDXDIR=${OUTDIR}/idx
    RESULTDIR=${OUTDIR}/${NAME}

    mkdir -p "$LOGDIR" "$IDXDIR" "$RESULTDIR"

    echo "[$(date)] Processing $NAME..." | tee -a "$LOGDIR/${NAME}.log"

    if [ -f "${INPUT}.idx" ]; then
        echo "[$(date)] Removing old index for $NAME" >> "$LOGDIR/${NAME}.log"
        rm -f "${INPUT}.idx"
    fi

    defense-finder run "$INPUT" \
        -o "$RESULTDIR" \
        --db-type unordered \
        --workers 0 \
        &>> "$LOGDIR/${NAME}.log"

    if [ ! -f "$RESULTDIR/all_best_solutions.tsv" ]; then
        echo "[$(date)] WARNING: DefenseFinder may have failed for $NAME (no all_best_solutions.tsv)" >> "$LOGDIR/${NAME}.log"
    fi

    IDX_FILE="${INPUT}.idx"
    if [ -f "$IDX_FILE" ]; then
        mv "$IDX_FILE" "$IDXDIR"
    else
        echo "[$(date)] WARNING: idx file not found for $NAME (expected at $IDX_FILE)" >> "$LOGDIR/${NAME}.log"
    fi
}

export -f doit

echo "[$(date)] Starting DefenseFinder batch annotation..."

echo "Contig type: chromosome"
parallel -j12 doit ::: Process/03.Defense/02.DefenseFinder/chromosome/chromosome_faa/*.faa ::: chromosome

echo "Contig type: plasmid"
parallel -j12 doit ::: Process/03.Defense/02.DefenseFinder/plasmid/plasmid_faa/*.faa ::: plasmid

echo "Contig type: phage"
parallel -j12 doit ::: Process/03.Defense/02.DefenseFinder/phage/phage_faa/*.faa ::: phage

echo "[$(date)] All DefenseFinder annotation completed."

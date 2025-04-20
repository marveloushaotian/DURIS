#!/bin/bash
# Please make sure to activate the appropriate environment first:
# conda activate cctyperv.1.6.4
doit() {
    INPUT="$1"      # Path to .fasta input file
    TYPE="$2"       # contig type: chromosome / plasmid / phage
    PROD_MODE="$3"  # Prodigal mode: meta / single
    
    # 创建更独特的目录名
    NAME=$(basename "$INPUT" | sed 's/\.fasta\(\.gz\)\{0,1\}$//')
    TIMESTAMP=$(date +%Y%m%d_%H%M%S_%N)
    UNIQUE_ID="${NAME}_${TIMESTAMP}_$$_${RANDOM}"
    
    # 修改目录结构，避免冲突
    BASE_DIR="Process/03.Defense/03.CRISPRCasTyper"
    OUTDIR="${BASE_DIR}/${TYPE}/results"
    LOGDIR="${BASE_DIR}/${TYPE}/logs"
    RESULTDIR="${OUTDIR}/${UNIQUE_ID}"
    FINAL_DIR="${BASE_DIR}/${TYPE}/${NAME}"
    
    mkdir -p "$LOGDIR" "$OUTDIR"
    
    echo "[$(date)] Running CCTyper on $NAME with unique ID $UNIQUE_ID..." | tee -a "$LOGDIR/${NAME}.log"
    
    # 运行CCTyper，使用唯一的目录名
    cctyper "$INPUT" "$RESULTDIR" \
        --no_plot \
        -t 1 \
        --prodigal "$PROD_MODE" \
        &>> "$LOGDIR/${NAME}.log"
    
    if [ $? -eq 0 ]; then
        echo "[$(date)] CCTyper completed successfully for $NAME" | tee -a "$LOGDIR/${NAME}.log"
        
        # 如果需要，将结果移动到标准位置
        if [ -d "$FINAL_DIR" ]; then
            echo "[$(date)] Removing existing directory $FINAL_DIR" | tee -a "$LOGDIR/${NAME}.log"
            rm -rf "$FINAL_DIR"
        fi
        
        echo "[$(date)] Moving results from $RESULTDIR to $FINAL_DIR" | tee -a "$LOGDIR/${NAME}.log"
        mv "$RESULTDIR" "$FINAL_DIR"
    else
        echo "[$(date)] ERROR: CCTyper failed for $NAME" | tee -a "$LOGDIR/${NAME}.log"
    fi
}
export -f doit
echo "[$(date)] Starting CRISPRCasTyper batch annotation..."
# chromosome
# echo "Contig type: chromosome"
# parallel -j8 doit ::: Process/03.Defense/03.CRISPRCasTyper/chromosome/split_chromosome/*.fasta ::: chromosome ::: meta
# plasmid
# echo "Contig type: plasmid"
# parallel -j8 doit ::: Process/03.Defense/03.CRISPRCasTyper/plasmid/split_plasmid/*.fasta ::: plasmid ::: meta
# phage
echo "Contig type: phage"
parallel -j8 doit ::: Process/03.Defense/03.CRISPRCasTyper/phage/split_phage/*.fasta ::: phage ::: meta
echo "[$(date)] All CCTyper annotation completed."

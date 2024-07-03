#!/bin/bash

# Activate the conda environment
# conda activate metaphlan3

# Function: Process each pair of FASTQ files and run Metaphlan
doit() {
    local fastq1=$1
    local fastq2=$2
    local output_dir=$3

    # Extract the sample name
    local name=$(basename ${fastq1} _qc_1.fastq.gz)
    local bowtie2_output="${output_dir}/${name}.bowtie2.bz2"
    local profile_output="${output_dir}/${name}_profiled.txt"

    echo "Processing ${name}..."
    
    # Create the output directory if it does not exist
    mkdir -p ${output_dir}

    # Run Metaphlan
    metaphlan ${input_dir}/${fastq1},${input_dir}/${fastq2} \
        --bowtie2out ${bowtie2_output} \
        --nproc 5 \
        --input_type fastq \
        -o ${profile_output} \
        &> ${output_dir}/${name}.log

    echo "${name} processing complete."
}

export -f doit

# Set input and output directories
input_dir="Source/01_rawreads/metagenome_qc"
output_dir="Process/06.Bacteria_taxonomy/metaphlan"

# Find all _qc_1.fastq.gz files
fastq_files=($(find ${input_dir} -name "*_qc_1.fastq.gz"))

# Use parallel to process all pairs of FASTQ files concurrently
echo "Starting Metaphlan analysis for paired-end FASTQ files..."

echo "contigs: metagenome chromosome"

parallel -j40 doit ::: ${fastq_files[@]} :::+ ${fastq_files[@]//_qc_1.fastq.gz/_qc_2.fastq.gz} ::: ${output_dir}

echo "All Metaphlan analyses are complete."


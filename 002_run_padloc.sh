#!/bin/bash

# Function to display help message
show_help() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -h, --help            Show this help message and exit"
  echo "  --fasta_dir=DIR       Specify the directory containing the fasta files"
  echo "  --results_dir=DIR     Specify the directory where results will be saved"
}

# Parse command-line options
while :; do
  case $1 in
    -h|--help)
      show_help
      exit
      ;;
    --fasta_dir=?*)
      fasta_dir=${1#*=}
      ;;
    --results_dir=?*)
      results_dir=${1#*=}
      ;;
    *)
      break
  esac
  shift
done

# Check if both directories are set
if [ -z "$fasta_dir" ] || [ -z "$results_dir" ]; then
  echo "ERROR: Both fasta_dir and results_dir must be specified."
  exit 1
fi

# Load any required modules or environments
source activate padloc

# Perform the main tasks
for fasta_file in ${fasta_dir}/*.fasta; do
  padloc --fna "$fasta_file" --outdir "${results_dir}" &
done

# Wait for all background tasks to finish
wait


import os
import gzip
import argparse

def process_files(input_folder, output_folder, threshold):
    """
    Process coverage and profile files to generate abundance statistics for contigs.
    
    Args:
        input_folder (str): Path to the folder containing coverage and profile files
        output_folder (str): Path to the folder where output files will be saved
        threshold (float): Coverage threshold for filtering contigs
        
    The function processes pairs of files:
    - *_coverage.txt.gz: Contains coverage information for contigs
    - *_profile.txt.gz: Contains abundance profiles
    """
    for file_name in os.listdir(input_folder):
        # Process files ending with _coverage.txt.gz
        if file_name.endswith("_coverage.txt.gz"):
            # Extract sample name by removing the suffix (14 characters)
            sample_name = file_name[:-16]
            
            # Construct file paths
            coverage_file = os.path.join(input_folder, file_name)
            profile_file = os.path.join(input_folder, sample_name + "_profile.txt.gz")
            output_file = os.path.join(output_folder, sample_name + "_existing_contigs_ab_per_sample.txt")
            
            # Dictionary to store contigs passing coverage threshold
            dictlt = {}
            
            # Process coverage file
            with gzip.open(coverage_file, 'rt') as infile:
                for line in infile:
                    lst = line.strip().split()
                    # Filter contigs based on coverage threshold
                    if float(lst[1]) > float(threshold):
                        dictlt[lst[0]] = lst[0]
            
            # Process profile file and write results
            with gzip.open(profile_file, 'rt') as infile:
                with open(output_file, 'w') as outfile:
                    # Skip header lines (first 11 lines)
                    for i in range(11):
                        infile.readline()
                    
                    # Process each contig
                    for line in infile:
                        lst = line.strip().split()
                        try:
                            # If contig passed coverage threshold, write its abundance
                            st = "{}\t{}\n".format(dictlt[lst[0]], lst[1])
                            outfile.write(st)
                        except:
                            # If contig didn't pass threshold, write zero abundance
                            st = "{}\t{}\n".format(lst[0], 0)
                            outfile.write(st)

if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="Process coverage and profile files for contig abundance analysis.")
    parser.add_argument("-i", "--input", 
                       required=True, 
                       help="Input folder containing coverage and profile files.")
    parser.add_argument("-o", "--output", 
                       required=True, 
                       help="Output folder for processed abundance files.")
    parser.add_argument("-t", "--threshold", 
                       type=float, 
                       default=0.55, 
                       help="Coverage threshold for filtering contigs (default: 0.55).")
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # Run the processing function
    process_files(args.input, args.output, args.threshold)

import argparse

def split_gff(input_gff, output_with_dms, output_without_dms):
    # Open the input GFF file and the two output files
    with open(input_gff, 'r') as infile, \
         open(output_with_dms, 'w') as with_dms, \
         open(output_without_dms, 'w') as without_dms:
        
        # Iterate over each line in the input GFF file
        for line in infile:
            # Skip comment lines
            if line.startswith('#'):
                continue
            
            # Check if the line contains 'DMS_others'
            if 'DMS_other' in line:
                with_dms.write(line)
            else:
                without_dms.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a GFF file based on the presence of 'DMS_others'.")
    parser.add_argument("-i", "--input_gff", required=True, help="Input GFF file path")
    parser.add_argument("-d", "--output_with_dms", required=True, help="Output GFF file path for lines containing 'DMS_others'")
    parser.add_argument("-o", "--output_without_dms", required=True, help="Output GFF file path for the remaining lines")
    
    args = parser.parse_args()
    
    split_gff(args.input_gff, args.output_with_dms, args.output_without_dms)


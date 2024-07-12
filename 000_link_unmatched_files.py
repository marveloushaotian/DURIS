import os
import argparse
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_base_names(directory, extension):
    """
    Extract unique base names from the filenames in a directory,
    excluding a specified extension.

    Parameters:
    directory (str): Path to the directory.
    extension (str): File extension to exclude from the base name.

    Returns:
    set: A set of unique base names.
    """
    base_names = set()
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            base_name = filename[:-len(extension)]
            base_names.add(base_name)
    return base_names

def main():
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="Script to copy unmatched symbolic links from Directory 2 to Directory 3."
    )
    parser.add_argument(
        '-d1', '--directory1', required=True, 
        help="Path to Directory 1. This is used to extract base names for matching."
    )
    parser.add_argument(
        '-d2', '--directory2', required=True, 
        help="Path to Directory 2. This is used to find symbolic links with filenames that do not match those in Directory 1."
    )
    parser.add_argument(
        '-d3', '--directory3', required=True, 
        help="Path to Directory 3. This is the destination directory where unmatched symbolic links from Directory 2 will be copied."
    )
    parser.add_argument(
        '-e', '--extension', required=True, 
        help="File extension to use for extracting base names in Directory 1, e.g., .sam, .bam."
    )
    args = parser.parse_args()

    directory1 = args.directory1
    directory2 = args.directory2
    directory3 = args.directory3
    extension = args.extension

    logging.info(f"Extracting base names from Directory 1 using extension '{extension}'")
    base_names_dir1 = extract_base_names(directory1, extension)

    logging.info("Identifying non-matching symbolic links in Directory 2")
    non_matching_links = []
    for filename in os.listdir(directory2):
        if filename.endswith('_qc_2.fastq.gz') or filename.endswith('_qc_1.fastq.gz'):
            base_name = filename.rsplit('_', 2)[0]
            if base_name not in base_names_dir1:
                src_path = os.path.join(directory2, filename)
                if os.path.islink(src_path):  # Ensure it's a symbolic link
                    non_matching_links.append(filename)

    logging.info(f"Found {len(non_matching_links)} non-matching symbolic links")

    os.makedirs(directory3, exist_ok=True)

    logging.info(f"Copying non-matching symbolic links to {directory3}")
    for filename in tqdm(non_matching_links, desc="Copying links"):
        src = os.path.join(directory2, filename)
        dst = os.path.join(directory3, filename)
        if not os.path.exists(dst):
            target_path = os.readlink(src)
            os.symlink(target_path, dst)
            logging.info(f"Created symlink for {filename}")

if __name__ == "__main__":
    main()


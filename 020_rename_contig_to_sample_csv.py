import pandas as pd
import argparse

def process_csv_data(input_file_path, output_file_path, id_column='ID', sample_column='Sample_Name'):
    """
    Process CSV file to extract and transform sample names from ID column.
    
    Parameters:
    -----------
    input_file_path : str
        Path to input CSV file
    output_file_path : str
        Path where processed CSV file will be saved
    id_column : str
        Name of the column containing IDs (default: 'ID')
    sample_column : str
        Name of the new column to be created for sample names (default: 'Sample_Name')
    """
    try:
        # Load the CSV file
        data = pd.read_csv(input_file_path)
        print(f"Successfully loaded {input_file_path}")
        
        # Function to extract sample name from ID
        def extract_sample_name(id_value):
            """
            Extract sample name from ID following specific patterns.
            Modify this function according to your ID pattern.
            """
            try:
                if pd.isna(id_value):
                    return None
                    
                id_str = str(id_value).strip()
                
                # Pattern matching for different ID formats
                if id_str.startswith('18097D'):
                    parts = id_str.split('-')
                    if len(parts) >= 3:
                        number_part = ''.join(filter(str.isdigit, parts[2]))
                        return f'Sample_{int(number_part):02d}' if number_part else None
                        
                elif id_str.startswith('DP'):
                    parts = id_str.split('-')
                    if len(parts) >= 2:
                        number_part = ''.join(filter(str.isdigit, parts[1]))
                        return f'Sample_{int(number_part):02d}' if number_part else None
                        
                return None
                
            except Exception as e:
                print(f"Error processing ID {id_value}: {str(e)}")
                return None

        # Apply the extraction function and create new column
        data[sample_column] = data[id_column].apply(extract_sample_name)
        
        # Count successful transformations
        successful_transforms = data[sample_column].notna().sum()
        total_rows = len(data)
        
        print(f"Successfully processed {successful_transforms} out of {total_rows} rows")
        
        # Save the processed data
        data.to_csv(output_file_path, index=False)
        print(f"Processed data saved to {output_file_path}")
        
        # Return summary statistics
        return {
            'total_rows': total_rows,
            'processed_rows': successful_transforms,
            'success_rate': f"{(successful_transforms/total_rows)*100:.2f}%"
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

def main():
    """
    Main function to handle command line arguments and execute the processing.
    """
    parser = argparse.ArgumentParser(description='Process CSV file to extract sample names from IDs')
    
    parser.add_argument('--input_file', 
                       type=str, 
                       required=True, 
                       help='Path to the input CSV file')
                       
    parser.add_argument('--output_file', 
                       type=str, 
                       required=True, 
                       help='Path to save the processed CSV file')
                       
    parser.add_argument('--id_column', 
                       type=str, 
                       default='ID',
                       help='Name of the column containing IDs (default: ID)')
                       
    parser.add_argument('--sample_column', 
                       type=str, 
                       default='Sample_Name',
                       help='Name of the new column for sample names (default: Sample_Name)')

    args = parser.parse_args()

    # Process the file and get statistics
    stats = process_csv_data(
        args.input_file,
        args.output_file,
        args.id_column,
        args.sample_column
    )
    
    # Print summary statistics
    print("\nProcessing Summary:")
    print(f"Total rows processed: {stats['total_rows']}")
    print(f"Successful transformations: {stats['processed_rows']}")
    print(f"Success rate: {stats['success_rate']}")

if __name__ == '__main__':
    main()

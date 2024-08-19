import pandas as pd
import argparse

def find_unique_defense_types(input_file, output_file, countries, locations, classifications, exclude_pdc):
    # 读取文件
    df = pd.read_csv(input_file, sep='\t')

    # 可选地筛选掉Defense_Type列中开头为PDC的行
    if exclude_pdc:
        df = df[~df['Defense_Type'].str.startswith('PDC')]

    # 过滤条件
    filtered_df = df.copy()
    if countries:
        country_list = countries.split(',')
        filtered_df = filtered_df[filtered_df['Country'].isin(country_list)]
    if locations:
        location_list = locations.split(',')
        filtered_df = filtered_df[filtered_df['Location_BAF'].isin(location_list)]
    if classifications:
        classification_list = classifications.split(',')
        filtered_df = filtered_df[filtered_df['Contig_Classification'].isin(classification_list)]

    # 获取满足条件的Defense_Type
    filtered_defense_types = filtered_df['Defense_Type'].unique()

    # 找到这些Defense_Type在整个数据集中的出现次数
    defense_type_counts = df['Defense_Type'].value_counts()

    # 找到仅在过滤条件中存在的Defense_Type
    unique_defense_types = []
    for dt in filtered_defense_types:
        # 获取Defense_Type在过滤后的数据中的行数
        filtered_count = filtered_df[filtered_df['Defense_Type'] == dt].shape[0]
        # 获取Defense_Type在整个数据集中的行数
        total_count = defense_type_counts[dt]
        # 如果在过滤后的数据和整个数据集中行数相同，则表示仅在过滤条件中出现
        if filtered_count == total_count:
            # 检查是否仅在指定的条件中存在
            dt_countries = df[df['Defense_Type'] == dt]['Country'].unique()
            dt_locations = df[df['Defense_Type'] == dt]['Location_BAF'].unique()
            dt_classifications = df[df['Defense_Type'] == dt]['Contig_Classification'].unique()
            if (not countries or set(dt_countries) == set(country_list)) and \
               (not locations or set(dt_locations) == set(location_list)) and \
               (not classifications or set(dt_classifications) == set(classification_list)):
                unique_defense_types.append(dt)

    # 输出独有的Defense_Type
    if not unique_defense_types:
        print("No unique Defense_Type found for the specified conditions.")
    else:
        print("Unique Defense_Type(s) for the specified conditions:")
        for dt in unique_defense_types:
            print(dt)
        
        # 如果指定了输出文件，则保存结果到输出文件
        if output_file:
            with open(output_file, 'w') as f:
                for dt in unique_defense_types:
                    f.write(f"{dt}\n")
            print(f"Unique Defense_Type(s) have been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find unique Defense_Type based on specified conditions.')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('-c', '--countries', help='Comma-separated list of countries to filter')
    parser.add_argument('-l', '--locations', help='Comma-separated list of Location_BAF to filter')
    parser.add_argument('-cc', '--classifications', help='Comma-separated list of Contig_Classification to filter')
    parser.add_argument('--exclude_pdc', action='store_true', help='Exclude Defense_Type starting with PDC')
    args = parser.parse_args()

    find_unique_defense_types(args.input, args.output, args.countries, args.locations, args.classifications, args.exclude_pdc)


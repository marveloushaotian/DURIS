import pandas as pd
import argparse
from itertools import product, chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def find_unique_defense_types(input_file, output_file, locations, classifications, countries, exclude_pdc):
    # 读取文件
    df = pd.read_csv(input_file, sep='\t')

    # 可选地筛选掉Defense_Type列中开头为PDC的行
    if exclude_pdc:
        df = df[~df['Defense_Type'].str.startswith('PDC')]

    # 生成所有可能的单个条件组合
    location_list = locations.split(',') if locations else []
    classification_list = classifications.split(',') if classifications else []
    country_list = countries.split(',') if countries else []
    single_conditions = list(product(location_list, classification_list, country_list))

    # 生成所有可能的组合子集，包括跨越多个条件的组合
    all_combinations = list(powerset(single_conditions))

    # 创建一个字典来存储每个Defense_Type出现的组合
    defense_type_combinations = {comb: set() for comb in all_combinations}

    # 对每个Defense_Type，找出它出现的所有单个条件
    defense_type_conditions = {}
    for loc, cls, country in single_conditions:
        filtered_df = df[(df['Location_BAF'] == loc) & (df['Contig_Classification'] == cls) & (df['Country'] == country)]
        for dt in filtered_df['Defense_Type'].unique():
            if dt not in defense_type_conditions:
                defense_type_conditions[dt] = set()
            defense_type_conditions[dt].add((loc, cls, country))

    # 对每个组合，找出完全匹配该组合的Defense_Type
    for comb in all_combinations:
        for dt, conditions in defense_type_conditions.items():
            if set(comb) == conditions:
                defense_type_combinations[comb].add(dt)

    # 找到仅在特定组合中出现的Defense_Type，确保没有重叠
    unique_defense_types = {}
    used_defense_types = set()

    # 按子集大小降序排序，优先考虑更大的组合
    sorted_combinations = sorted(all_combinations, key=len, reverse=True)

    for comb in sorted_combinations:
        unique_dt_for_comb = set()
        for dt in defense_type_combinations[comb]:
            if dt not in used_defense_types:
                unique_dt_for_comb.add(dt)
                used_defense_types.add(dt)
        if unique_dt_for_comb:
            unique_defense_types[comb] = unique_dt_for_comb

    # 输出独有的Defense_Type
    if not unique_defense_types:
        print("No unique Defense_Type found for any combination of the specified conditions.")
    else:
        print("Unique Defense_Type(s) for different combinations of the specified conditions:")
        for comb, dt_set in unique_defense_types.items():
            print(f"\nCombination: {comb}")
            for dt in dt_set:
                print(f"  Defense_Type: {dt}")
                for loc, cls, country in comb:
                    count = df[(df['Defense_Type'] == dt) & (df['Location_BAF'] == loc) & (df['Contig_Classification'] == cls) & (df['Country'] == country)].shape[0]
                    print(f"    Location_BAF: {loc}, Contig_Classification: {cls}, Country: {country}, Count: {count}")

        # 如果指定了输出文件，则保存结果到输出文件
        if output_file:
            with open(output_file, 'w') as f:
                for comb, dt_set in unique_defense_types.items():
                    f.write(f"Combination: {comb}\n")
                    for dt in dt_set:
                        f.write(f"  Defense_Type: {dt}\n")
                        for loc, cls, country in comb:
                            count = df[(df['Defense_Type'] == dt) & (df['Location_BAF'] == loc) & (df['Contig_Classification'] == cls) & (df['Country'] == country)].shape[0]
                            f.write(f"    Location_BAF: {loc}, Contig_Classification: {cls}, Country: {country}, Count: {count}\n")
                    f.write("\n")
            print(f"Unique Defense_Type(s) have been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find unique Defense_Type based on all possible combinations of specified conditions.')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('-l', '--locations', help='Comma-separated list of Location_BAF to filter')
    parser.add_argument('-cc', '--classifications', help='Comma-separated list of Contig_Classification to filter')
    parser.add_argument('-c', '--countries', help='Comma-separated list of Country to filter')
    parser.add_argument('--exclude_pdc', action='store_true', help='Exclude Defense_Type starting with PDC')
    args = parser.parse_args()

    find_unique_defense_types(args.input, args.output, args.locations, args.classifications, args.countries, args.exclude_pdc)


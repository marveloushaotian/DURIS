import csv
import argparse

def read_mobile_contigs(file_path):
    mobile_contigs = set()
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过标题行
        for row in reader:
            mobile_contigs.add(row[0])  # 假设第一列是contig名称
    return mobile_contigs

def filter_fasta(fasta_path, mobile_contigs, output_path):
    with open(fasta_path, 'r') as fasta_file, open(output_path, 'w') as output_file:
        write_next = False
        for line in fasta_file:
            if line.startswith('>'):
                contig_name = line.strip()[1:]  # 去除'>'符号
                if contig_name in mobile_contigs:
                    output_file.write(line)
                    write_next = True
                else:
                    write_next = False
            elif write_next:
                output_file.write(line)
                write_next = False

def main():
    parser = argparse.ArgumentParser(description='Filter FASTA file based on mobile contigs.')
    parser.add_argument('mobile_contigs', help='Path to the mobile_contigs.csv file')
    parser.add_argument('plasmid_fasta', help='Path to the plasmid.fasta file')
    parser.add_argument('output_fasta', help='Path for the output filtered FASTA file')
    
    args = parser.parse_args()

    mobile_contigs = read_mobile_contigs(args.mobile_contigs)
    filter_fasta(args.plasmid_fasta, mobile_contigs, args.output_fasta)
    print(f"筛选完成,结果已保存到 {args.output_fasta}")

if __name__ == "__main__":
    main()

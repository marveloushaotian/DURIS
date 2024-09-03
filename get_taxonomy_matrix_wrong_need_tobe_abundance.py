import pandas as pd

# 定义样本和Phylum的顺序
samples = ["Sample_01", "Sample_02", "Sample_03", "Sample_04", "Sample_06", "Sample_07", "Sample_08", "Sample_09", 
           "Sample_11", "Sample_12", "Sample_13", "Sample_14", "Sample_16", "Sample_17", "Sample_18", "Sample_20", 
           "Sample_21", "Sample_22", "Sample_24", "Sample_25", "Sample_26", "Sample_28", "Sample_29", "Sample_30", 
           "Sample_32", "Sample_33", "Sample_34", "Sample_36", "Sample_37", "Sample_38", "Sample_40", "Sample_41", 
           "Sample_42", "Sample_43", "Sample_45", "Sample_46", "Sample_47", "Sample_48", "Sample_50", "Sample_51", 
           "Sample_52", "Sample_53", "Sample_55", "Sample_56", "Sample_57", "Sample_59", "Sample_60", "Sample_61", 
           "Sample_63", "Sample_64", "Sample_65", "Sample_67", "Sample_68", "Sample_69", "Sample_71", "Sample_72", 
           "Sample_73", "Sample_75", "Sample_76", "Sample_77", "Sample_05", "Sample_10", "Sample_15", "Sample_19", 
           "Sample_23", "Sample_27", "Sample_31", "Sample_35", "Sample_39", "Sample_44", "Sample_49", "Sample_54", 
           "Sample_58", "Sample_62", "Sample_66", "Sample_70", "Sample_74", "Sample_78"]

phylums = ["Abditibacteriota", "Acidobacteriota", "Actinomycetota", "Aquificota", "Armatimonadota", "Atribacterota", 
           "Bacillota", "Bacteroidota", "Balneolota", "Bdellovibrionota", "Caldisericota", "Calditrichota", 
           "Campylobacterota", "Candidatus_Absconditabacteria", "Candidatus_Bathyarchaeota", "Candidatus_Binatota", 
           "Candidatus_Bipolaricaulota", "Candidatus_Borrarchaeota", "Candidatus_Cloacimonadota", 
           "Candidatus_Cryosericota", "Candidatus_Culexarchaeota", "Candidatus_Deferrimicrobiota", 
           "Candidatus_Dormiibacterota", "Candidatus_Fervidibacterota", "Candidatus_Hadarchaeota", 
           "Candidatus_Korarchaeota", "Candidatus_Kryptoniota", "Candidatus_Lokiarchaeota", "Candidatus_Melainabacteria", 
           "Candidatus_Methylomirabilota", "Candidatus_Micrarchaeota", "Candidatus_Nanohalarchaeota", 
           "Candidatus_Omnitrophota", "Candidatus_Saccharibacteria", "Candidatus_Tectomicrobia", 
           "Candidatus_Thermoplasmatota", "Chlamydiota", "Chlorobiota", "Chloroflexota", "Chrysiogenota", 
           "Coprothermobacterota", "Cyanobacteriota", "Deferribacterota", "Deinococcota", "Dictyoglomota", 
           "Elusimicrobiota", "Euryarchaeota", "Fibrobacterota", "Fusobacteriota", "Gemmatimonadota", "Ignavibacteriota", 
           "Kiritimatiellota", "Lentisphaerota", "Mycoplasmatota", "Myxococcota", "Nitrososphaerota", "Nitrospinota", 
           "Nitrospirota", "Planctomycetota", "Pseudomonadota", "Rhodothermota", "Spirochaetota", "Synergistota", 
           "Thermodesulfobacteriota", "Thermodesulfobiota", "Thermomicrobiota", "Thermoproteota", 
           "Thermosulfidibacterota", "Thermotogota", "Verrucomicrobiota", "Vulcanimicrobiota"]

# 读取数据
df = pd.read_csv('all_defense_info_single_full_without_PDC_filtered_contig.txt', sep='\t')

# 创建一个空的DataFrame来存储计数
result = pd.DataFrame(0, index=phylums, columns=samples)

# 计算每个样本中每个Phylum的计数
for sample in samples:
    for phylum in phylums:
        count = len(df[(df['Sample'] == sample) & (df['Kaiju_Phylum'] == phylum)])
        result.loc[phylum, sample] = count

# 将结果写入文件
result.to_csv('nmds_taxonomy_withdf.txt', sep='\t')


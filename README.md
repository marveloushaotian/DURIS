# Link defense with Wastewater Plasmids
Genomic Evaluation of Natural Immunity Uncovered in Environmental Samples
https://github.com/marveloushaotian/GENIUS
## Requirements
- [x] Learning and Making the pipeline with Python and finishing **feasibility verification**.
  - [x] Understand the structure of given data.
  - [x] Understand the principle of mapping sequence back to qc reads.
  - [x] Understand the difference between different kinds of [[Gene abundance]] calculation selection.
- [x] Re-organize the file structure in the GitHub.
- [ ] Run the pipeline on the real data to get the defense system abundance table. Split the plasmidome and non-redundant. Only non-redundant groups need to get the abundance.
- [ ] Use R scripts to make downstream analyses on the real data.
- [ ] Make report slide.
  - [ ] Describe the project’s **background** using Figma, explain the data source, and provide detailed numbers.
  - [ ] Describe the **workflow** for processing the data, including the pre-processing, downstream analysis, and future analysis. Paste the code and calculating method.
  - [ ] Describe the **abundance** of all defense systems in the non-redundant and plasmidome groups.
  - [ ] The **diversity** of defense systems in different groups.
  - [ ] The **PCA** analyses.
  - [ ] **Statistic** analysis.
  - [ ] Link with **plasmids phenotype**. Plasmids type, length, inc family, and more?
  - [ ] Link with the transposon.
  - [ ] Discuss the **future** analysis plan.
## Pipeline
### Data Prepare
#### Plasmidome
* Located
`/home/projects/ku_00041/data/PEACE/Haotian/Project/GENIUS/Source/plasmidome_raw.`
* File name list
1. **all_linear_plasmidome.fasta**
2. **all_plasmidome_circular_plamsids.fasta**
3. all_plasmidome_circular [[MMseqs2]] results. [3]
4. all_plasmidome_circular [[BLAST]] results. [7] We don’t use these results.
5. all_plasmidome_linear [[MMseqs2]] results. [3]
The plasmidome DNA is extracted from the water samples and sent for sequencing. So, **each read represents a single plasmid.**
- [ ] Try mapping the reads back to [[NCBI]] and see what happens. It would be nice if the reads could map back to one or more plasmids in the database. Also, try learning how to use NCBI.
- [ ] What if we map the plasmidome sequence back to the QC data?
- [ ] Also, make a test for calculating map back abundance.
#### circular plasmids genome
Title
`DP-Sample001-S1-001_NODE_1_length_6376_cov_5.861738_cutoff_0_type_circular`
- [x] Which tools generate the file format like **NODE_1_length_6376_cov_5.861738**? To find out which step the sequence is. From [[SPAdes]]. That’s why every sequence has this kind of title.
#### linear plasmids genome
Title
`>DP-Sample016-S16-001_NODE_435_length_6621_cov_6.422784`
#### non-redundant
* Located
`/home/projects/ku_00041/data/PEACE/Haotian/Project/GENIUS/Source/non_redundant_raw`
* File name list
1. **non-redundant-gene-catalog.fasta**
2. non-redundant-gene-catalog [[MMseqs2]] results. [3]
3. non-redundant-gene-catalog [[BWA]] results. [5]
- [ ] **non-redundant-gene-catalog_rep_seq.fasta.faa**
- [ ] **non-redundant-gene-catalog_rep_seq.fasta.tsv**
The nonredundant plasmids are extracted from the metagenome sequence of water samples. So, each read represents.
Title
`>m_NODE_31_length_55761_cov_7.738341_35 # 41504 # 42352 # 1 # ID=31_35;partial=00;start_type=ATG;rbs_motif=AGxAG;rbs_spacer=5-10bp;gc`
Which have the information from [[Prodigal]].
### Extract defense systems
1. find the list of defense systems from the [[PADLOC/Output]] **padloc.csv** file.
2. combine all padloc.csv files by groups and use a script to clean the redundant titles. Get the **padloc_cleaned.csv** file for each group. (Script: `102_clean_redundant_raw.py`). Here, we divide the files into groups: ~*plasmidome_linear, plasmidome_circular, plasmidome_combined, and non-redundant.*~
3. filter defense systems records in padloc_cleaned.csv; ~this step is for the plasmidome group~, cause it can provide the direct defense counts number.(Script: `103_filter_defense_non_redundant.py`, `103_filter_defense_plasmidome.py`)
   1. **Filtering**: Reads the CSV, removing rows where 'system.number' is a duplicate header or 'system' equals '~DMS_other~'. The result is saved to an intermediary file. The suffix is **padloc_cleaned_filtered.csv**.
   2. **Transformation**: Loads the filtered data, generates a 'Unique_ID' by concatenating 'system.number' and 'seqid', and performs data aggregation: the suffix is **padloc_cleaned_filtered_transformed.csv**.
      * Retains the first occurrence of certain columns while ~calculating min/max for 'start'/'end'~ and ~counting 'Unique_ID'~ occurrences.
      * Extracts sample names from 'seqid' using regex, adds these as 'Sample', reorders columns to prioritize 'Sample', and saves the final dataset.
4. add the length and coverage as new columns from the transformed CSV files for each group. (Script: `104_addsuffix_length_and_coverage.py`). Here is the final table for downstream analyses.
5. extract the length information as a new column and keep the seqid. Please keep it for later use or never use it. (Script: `104_extract_id_and_length.py`).
---
6. Prepare the gff files for the extract sequence and split the gff files with DMS_other and others.
7. add the defense system information after the [[FASTA/FNA]] title and extract the specific defense systems sequence into a single file. ~This step is for the non-redundant group~. (Script: `106_extract_defense_sequence.py`) two different situations: for plasmidome or non-redundant results.
   1. for plasmidome: the plasmidome raw reads sequence has multiple raws, so we need to use `106_extract_defense_sequence_from_plasmidome.py`.
   2. for non-redundant: the non-redundant rew reads sequence only has one raw, so use `106_extract_defense_sequence_mutiple_inputs.py` and `106_run_mutiple_inputs.sh`.
   - [ ] **Be careful!** The defense systems read they are only part of the plasmidome raw sequence, so we must select the specific sequence based on the padloc.gff file. (and change the scripts also) The sequence in the non-redundant is almost 100% of the coverage.
8. In the end, we get defense systems list and defense systems sequence for all groups.
   - [ ] Should update the plasmidome defense system sequence.
   - [ ] Should update the DMS information for non-redundant defense system sequence.
- [ ] Try to map the plasmidome sequence back to the QC data. And see what happened.
---
- [x] Should we combine the results of the two parts? No, split them into two parts and wait for the next step.
### Map fasta files back to after qc files
**Please run in the same folder**
#### Use MMseqs to cluster and dereplicate the sequences provided.
`mmseqs easy-cluster {in} {prefix} tmp --min-seq-id 0.9 -c 0.95 --cov-mode 0`
The `{in}`  is the input file.
The `{prefix}` is the output file prefix.
#### Use [[BWA]] to map the sequence to the after QC reads.
**Build index**
`bwa index {prefix}_rep_seq.fasta`
Run it with the script: `202_bwa_build_index.py`.
---
**Run bwa alignment** (Need a long time)
`bwa mem -M {prefix}_rep_seq.fasta {sample}_qc_1.fastq.gz {sample}_qc_2.fastq.gz -t 8`
Run it in batch with the script: `203_bwa_mem_align.py`.
- [x] Check if the batch script works.
- [x] Change the batch script: remove the bwa_index.log and bwa_mem.log in the home folder.
- [x] Fix the bug: I can’t find the rep_seq file. Why?

**Use samtools to sort the bam file from the bwa result**
`samtools sort -n -@ 8 {sample}.bam -o {sample}_sort.bam`

**Use msamtools to filter the bam files**
`msamtools filter -b -l 80 -p 90 -z 80 --besthit {sample}_sort.bam >{sample}_sort_filter.bam`
- [ ] Is there another way to calculate? See how GPT works.

**Use msamtools to calculate the abundance**
`msamtools profile --multi=all --unit='fpkm' --label={sample}_sort_filter.bam -o {sample}_profile_rb.txt {sample}_sort_filter.bam`
- [ ] Test each method to calculate the gene abundance.
- [ ] Also, test the gpts method and Wanli method.

**Use msamtools to calculate the coverage**
`msamtools coverage -z --summary -o {sample}_sort_filter.bam {sample}_coverage_info.txt.gz`

**Calculate the abundance per sample and filter by the coverage meantime**
`209_abundance_per_sample.py`

**Combine all the abundance per sample information together**
`210_combine_all_abundance_info.py`

**Calculate the gene abundance**
- [ ] Compare the two methods.
- [ ] Why do we need to take the coverage into account?
### Downstream analyses
For plasmidome data, use the actual counts of defense systems from the PADLOC cause we have the group information at the beginning.
For non-redundant data, use the mapping abundance counts of defense systems cause they don’t have any group information.
#### Diversity, prevalence of defense systems.
**For plasmidome**
Barplot will show the diversity of all defense systems in each group.

**For non-redundant**

#### Comparison of defense systems in different groups.
PCA/NMDS/PCoA analyses for the different groups of the defense system.
Statistic analysis of defense system in different groups.
### GitHub scripts structure
* Source
  * non_redundant_faa_split_500000
  * non_redundant_fna_split_1000000
  * non_redundant_fna_split_60000
  * non_redundant_qc
  * non_redundant_raw
  * plasmidome_circular_fna_split_1000
  * plasmidome_linear_fna_split_1000
  * plasmidome_qc
  * plasmidome_raw
* Process
  * 01.PADLOC_find_defense_systems
    * 01.PADLOC_output
    * 02.Prepare_defense_list
  * 02.Map_defense_to_qc
* 0 prefix
  * Tool scripts.
* 1 prefix
  * Find defense systems and filter them.
* 2 prefix
  * Map the defense systems back to QC data.
* 9 prefix
  * Downstream analysis with R code.


- [ ] Update the readme in the GitHub.

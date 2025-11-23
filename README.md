# Discovering the Defense System in Urban Water Systems in EU Countries

![Diagram of a representative urban water system](https://github.com/user-attachments/assets/b7951960-fbf7-4f81-ad8c-71931fd9fd80)

## Background
Bacterial anti-phage defense systems play essential roles in microbial ecology, yet their dynamics within urban wastewater systems (UWS) remain poorly characterized.

## Results
In this study, we performed comprehensive metagenomic and plasmidome analyses on 78 wastewater samples collected during two seasons and four sampling points across UWS from three European countries. We observed a significant reduction in the abundance, diversity, and mobility potential of defense systems during biological treatment. However, these reductions were not directly correlated with changes in microbial abundance. Defense systems were significantly enriched on plasmids, particularly conjugative plasmids, where their gene density was approximately twice as high as on chromosomes and remained relatively stable across compartments. In contrast to chromosomal defense systems, plasmid-borne systems exhibited more frequent co-localization with a wide range of mobile genetic elements (MGEs)-associated genes, thereby facilitating multilayered dissemination networks. Furthermore, we detected a strong correlation between phage abundance and host defense system profiles, indicating ongoing phage-host co-evolutionary dynamics in these environments.

## Conclusions
In summary, our results demonstrate that UWS reduce the abundance and diversity of bacterial defense system genes. However, plasmid-associated defense systems can persist through shared mobile genetic reservoirs. These findings underscore the critical role of plasmids in bacterial immunity and provide new insights into defense system dynamics within urban wastewater environments.

**KEYWORDS**: Anti-Phage Defense Systems, Plasmid, Wastewater, Metagenome, Plasmidome

## Availability of Data and Materials
All the code can be found in this GitHub repository: https://github.com/marveloushaotian/DURIS.

All results and associated scripts can be found in this Google Drive:
https://drive.google.com/drive/folders/11hMwINQzWZnb6MNSJNY4AT9G3xdLEOaZ.

The original data tables used to support and reproduce the analysis are available in this Zenodo repository: https://doi.org/10.5281/zenodo.14883504.

The raw sequences used in this study are available on NCBI SRA at BioProject accession number PRJEB85938.

## Scripts Structure

`00X`: Common tools for processing the raw table.

`10X`: Common pipeline for sequence pre-processing, contig classification.

`20X`: Common pipeline for annotation.

`30X`: Basic scripts for processing the annotation table.

## Google Drive Folder Structure

`Collect`: Folder for processing the raw sequencing data. including the raw annotation table, the processing script, and the plots.
- `Collect/nr_contig`: Analysis results of the non-redundant contigs.
- `Collect/r_contig`: Analysis results of the redundant contigs.
- `Collect/xx`: The annotation results for each genes.

`Results`: Folder for storing the final results in the manuscript.

`Reports`: Folder for storing the regular report.

`Supplementary`: Folder for storing the supplementary information.

`Backup_Scripts`: Folder for storing the scripts that deprecated.

## Author Contributions
**H.Z.**: Investigation, Formal analysis, Data curation, Methodology, Visualization, Writing – original draft
**L.P.**: Conceptualization, Writing – review & editing, Formal analysis, Validation
**W.H.**: Formal analysis, Data curation, Software, Methodology
**M.R.M.**: Conceptualization, Methodology, Writing – review & editing, Validation
**L.Y.**: Conceptualization, Validation, Writing – review & editing, Formal analysis
**A.D.**: Writing – review & editing, Validation, Resources
**R.P.R.**: Writing – review & editing, Validation, Methodology
**J.N.**: Writing – review & editing, Validation, Supervision
**S.J.S.**: Conceptualization, Funding acquisition, Supervision, Project administration, Resources, Writing – review & editing

## Funding
This work was supported by the NNF-funded project pTracker (NNF20OC0062223) awarded to S.J.S.
H.T.Z. was funded by the China Scholarship Council (202104910071).
L.P. and R.P.-R. were supported by a research grant (VIL60763) from VILLUM FONDEN.

## Competing Interests
The authors declare no competing interests.

## Acknowledgments
We hereby acknowledge the support of the NNF-funded project pTracker (NNF20OC0062223), awarded to S.J.S. H.T.Z. was funded by a scholarship from China Scholarship Council (202104910071). L.P. and R.P.-R. were supported by a research grant (VIL60763) from VILLUM FONDEN.

## Contact
Haotian Zheng - haotian.zheng@bio.ku.dk, marveloushaotian@icloud.com

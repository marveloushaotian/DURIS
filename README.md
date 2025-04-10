# Discovering the defense system in urban water systems in EU countries.

## About this project

- This is a project finding defense systems in urban water systems in EU countries.
- We are collecting waste water from wastewater treatment plants (WWTP) in Denmark, Spain, and
  United Kingdom. In each country, we are collecting waste water in four different locations: the
  Hospital sewage, the residential sewage, the mixed sewage, and the biological treatment basin. In
  the end we got 78 samples.
- Sequencing the waste water with metagenomic and plasmid sequencing.

![Diagram of a representative urban water system](https://github.com/user-attachments/assets/b7951960-fbf7-4f81-ad8c-71931fd9fd80)

## Build with

For raw sequencing data, use python and shell. For statistic analysis and ploting, use R and python.
The code for raw sequencing data processing is stored in the github repository. the code for ploting
and statistic analysis is stored in the google drive.
Link to the project google drive:
https://drive.google.com/drive/folders/1OUcSnWUKoblLPLznPogyRXmWmJovP0d2?usp=sharing

## Scripts Structure

00X: Common tools for processing the raw table.

10X: Common pipeline for sequence pre-processing, contig classification.

20X: Common pipeline for annotation.

30X: Basic scripts for processing the annotation table.

## Google Drive Folder Structure

Collect: Folder for processing the raw sequencing data. including the raw annotation table, the
processing script, and the plots.

Collect/nr_contig: Analysis results of the non-redundant contigs.

Collect/r_contig: Analysis results of the redundant contigs.

Collect/xx: The annotation results for each genes.

Results: Folder for storing the final results in the manuscript.

Reports: Folder for storing the regular report.

Supplementary: Folder for storing the supplementary information.

Backup_Scripts: Folder for storing the scripts that deprecated.

## Contributing

Haotian Zheng wrote the manuscript and excute the data classification, annotation, statistic, and
ploting. Professor Søren Johannes Sørensen and Associate Professor Rafael Pinilla-Redondo worte the grant, Wanli He excute the plasmids
annotation, Lili Yang, Joseph Nesme and Mario Rodríguez Mestre helped with discussion.

## Contact

Haotian Zheng - haotian.zheng@bio.ku.dk, marveloushaotian@icloud.com

## Acknowledgments

Thanks for Professor Søren, Associate Professor Rafael, and Lili Yang, Wanli He, Joseph Nesme,
Mario Rodríguez Mestre for their help and suggestions.

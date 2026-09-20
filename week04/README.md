# Week 4: Downloading and QC-checking SRA reads for GCA_027936885.1 / JN542536.1

This project continues the genome selected in Week 2 ILTV[Downloading a genome assembly from NCBI (Gallid alphaherpesvirus 1)](week02_ILTV/README.md). 

The assembled genome corresponds to NCBI assembly: GCA_027936885.1, which corresponds to the accession JN542536.1 in genbank. The goal of this assignment was to locate public sequencing data for that genome, download a subset of reads from the Sequence Read Archive (SRA), and perform a simple quality-control workflow.

## Genome choice

The selected genome is:

- Assembly accession: GCA_027936885.1
- GenBank/RefSeq accession: JN542536.1
- SRA accession: SRR29869142

## Popularity of Gallid alphaherpesvirus 1 (infectious laryngotracheitis virus)

Breakdown of SRA datasets: [NCBI SRA datasets for ILTV](https://www.ncbi.nlm.nih.gov/sra?term=%28%22Gallid%20alphaherpesvirus%201%22%5BOrganism%5D%20OR%20%28%22Gallid%20alphaherpesvirus%201%22%5BOrganism%5D%20OR%20infectious%20laryngotracheitis%20virus%5BAll%20Fields%5D%29%29%20AND%20cluster_public%5Bprop%5D&cmd=DetailsSearch).

Total datasets
    - 57

Platform

    - 31 Illumina

    - 26 Oxford Nanopore

Types of data

    - 26 Oxford Nanopore amplicon sequencing of partial genomes 

    - 15 RNA seq of host transcriptome during infection

    - 16 WGS of ILTV (Illumina)


Unfortunately, a majority of sequenced ILTV data is not represented in the SRA; see the NCBI genome dataset page: [NCBI genome datasets for ILTV](https://www.ncbi.nlm.nih.gov/datasets/genome/?taxon=10386).

File type breakdown

    - 45 fastq (Oxford Nanopore amplicon seq, illumina WGS, illumina RNAseq)

    - 12 bam format (Illumina RNAseq)

Compared to gallid alphaherpesvirus 2 (Mareks Disease Virus), there are far less genomes (16 vs ~200) and RNAseq data for ILTV: [NCBI SRA datasets for MDV](https://www.ncbi.nlm.nih.gov/sra?term=MDV%5BAll%20Fields%5D%20OR%20%28%22Gallid%20alphaherpesvirus%202%22%5BOrganism%5D%20OR%20Mareks%20Disease%20virus%5BAll%20Fields%5D%29%20OR%20%28%22Gallid%20alphaherpesvirus%202%22%5BOrganism%5D%20OR%20Gallid%20alphaherpesvirus%202%5BAll%20Fields%5D%29&cmd=DetailsSearch).


## Downloading a subset of reads from the SRA

# Automating variant calling between genomes

## Overview

This is an updated script from (url:https://github.com/DKehlbeck/BMMB852-2026/blob/main/week08/Makefile) to download reads from given SRA accession numbers, map them to the NCBI reference genome and identify sites of difference. 

Updates / alterations include the use of a design.csv file to act as input for multiple accession numbers for both a BioProject accession or a SRR accession, as well as your input fasta reference. A python script is used to parse the design.csv accession numbers and pull out all SRR numbers associated with the given BioProject, then append them with any individually listed SRR accession numbers.

The currently listed design.tsv will download the ILTV (Infectious Laryngeotitis Virus) NCBI reference genome, SA2 ([GCF_008787145.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_008787145.1/)), along with the reads associated with the BioProject: Genome sequencing of Gallid alphaherpesvirus 1 (ILTV) US field and vaccine strains ([PRJNA1136498](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA1136498)). Additionally, two other ILTV strains were included as individual SRR numbers: an additional vaccine strain ([SRR29859430](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR29859430&display=metadata)) and another strain from outside of the US ([SRR8282614](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR8282614&display=metadata)).

However, it should be adaptable to any other set of refernece or SRR genomes
## Script execution

### Fill the design.csv

Design file structure is as follows with the first column representing the accession number

    - Assembly accession
    - SRR or BioProject accession

The second column should contain whether that will be used as the reference genome, for all reads to map to and use for variant calling, or as a set of samples to identify read supported variants with. As mentioned previously these can either be in the form of a BioProject accession number or individually listed SRR numbers.


Current Example:

```bash
Accession,type
GCF_008787145.1,reference
SRR8282614,sample
PRJNA1136498,sample
SRR29859430,sample
```

### Change makefile input parameters

Not included in the design file are the input parameters such as:

```bash
# N Number of reads per SRR to download
N       ?= 500000
# Adapter sequence for removal if present
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
# Number of core threads to use for eventual mapping & variant calling
THREADS ?= 4
```

### Execution

To execute the whole pipeline:

```bash
make all
```

For information following the run on genomes included and file locations

```bash
make info
```

If you want to confirm SRR accessions:

```bash
python parse_accessions.py
```

Additionally, this can be ediited prior to make all if you have any additional changes.

The sample rule supports both paired-end reads (`*_1.fastq` and `*_2.fastq`) and single-end reads. For single-end runs, it recognizes either `*_1.fastq` or the unnumbered `*.fastq` file produced by `fastq-dump --split-files`.


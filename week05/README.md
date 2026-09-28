# Generating a bam file from downloaded fasta & fastq 

This weeks goal was to use scripts in week02 and week04 to download a assemebled genome and align corresponding reads to generate a bam file. 

The assembled genome was pulled from genbank here:
[Strain 63140 genome assembly](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_027936885.1/)

The paired end reads were pulled from the short read archive here:
[SRA accession SRR29869142](https://www.ncbi.nlm.nih.gov/sra/?term=SRR29869142)

## Usage and Execution

### Input information

```bash
ASSEMBLY_NAME ?= ILTV-63140
ASSEMBLY_ACCESSION ?= GCA_027936885.1
NCBI_FTP_URL ?= https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/027/936/885/GCA_027936885.1_ASM2793688v1
SRA_ACCESSION ?= SRR29869142
# N represents the number of reads to download
N ?= 16400
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
THREADS ?= 4
```

### Executation

```bash
dirs: ## Create output directories (fastq, fasta, gff, metadata, fastp, alignments)
genome: dirs ## Download genome FASTA + GFF and NCBI metadata (README, assembly report/stats, md5s)
sra: dirs ## Download first N reads from SRA, rename to R1/R2, save seqkit stats + SRA metadata
trim: sra ## Trim adapters and low-quality tails with fastp (HTML + JSON reports)
index: genome ## Build BWA index and samtools .fai for the reference
align: index trim ## Align trimmed reads with BWA-MEM -> sorted, indexed BAM + flagstat + coverage
clean: ## Delete all downloaded and generated data
```

## Determining the Number of Reads for ~10x Coverage

| Parameter | Value |
| --- | ---: |
| Genome length | 153,633 bp |
| Average read length after QC | 94 bp |
| Paired-end reads | Yes (2 reads per pair) |
| Target coverage | 10x |

Coverage is calculated as:

$$
C = \frac{L \times R \times N}{G}
$$

Using the values above:

$$
10 = \frac{94 \times 2 \times N}{153{,}633}
$$

Solving for the number of read pairs:

$$
N = \frac{10 \times 153{,}633}{94 \times 2} \approx 8{,}171 \text{ read pairs}
$$

OR

~16,400 reads

## Statistics reports

Baseline statistics report for read mapping information generated with samtools flagstat:

```bash
samtools flagstat alignments/*.bam
```
flagstat output:

```bash
31362 + 0 in total (QC-passed reads + QC-failed reads)
31362 + 0 primary
0 + 0 secondary
0 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
2731 + 0 mapped (8.71% : N/A)
2731 + 0 primary mapped (8.71% : N/A)
31362 + 0 paired in sequencing
15681 + 0 read1
15681 + 0 read2
2704 + 0 properly paired (8.62% : N/A)
2708 + 0 with itself and mate mapped
23 + 0 singletons (0.07% : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)
```

Relative coverage plot generated using:

```bash
samtools coverage -m alignments/*.bam
```

Samtools coverage plot:
![Relative coverage track for N=16,000 reads](images/N16000_relative_coverage_track_2026-09-28%20094438.png)

IGV coverage: 
![Sporadic coverage for mapped reads](<images/IGV_230831.png>)

### Comments

Average coverage is well below the expected 10x, however, this is likely due to a low percentage of reads mapping (~8.71%). This number varied from 8-20% when the makefile was run repeatedly to download a different set of reads so there may be some variability in which reads are downloaded that may have intrinsicially lower ability to map to the genome.

When all reads are taken for mapping, there is still only ~23% of reads mapping to the genome. A majoirty of unmapped reads are signficiantly shorter than the 94bp mean. To investigate whether there may still be subsatntial host reads I blasted a few poorly mapped reads, but were still identified as ILTV so a more indepth taxonomic classifcation may be requiured to rule that out.

Coverage is very sporadic - likely impart due to random sampling. A representative image of the attempted 10x coverage is seen above. To test whether this is maintained when a majority of the reads are included, the N was adjusted:

```bash
N ?= 13000000
```
 
Coverage distribution is more uniform when nearly all SRA reads are taken (see below)


## Investigating low mapping

Pulling all of the reads ~13,000,000 from SRA improved coverage subsatantially to 4,000x, but still sat at ~23% of reads mapping. 

![Improved coverage for all reads](images/full_relative_coverage_track_2026-09-28%20093428.png)

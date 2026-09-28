SHELL := /bin/bash
 
# Input variables
ASSEMBLY_NAME ?= ILTV-63140
ASSEMBLY_ACCESSION ?= GCA_027936885.1
NCBI_FTP_URL ?= https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/027/936/885/GCA_027936885.1_ASM2793688v1
SRA_ACCESSION ?= SRR29869142
# N represents the number of reads to download
N ?= 60000
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
THREADS ?= 4
 
# Output directories
FASTQ_DIR      := fastq
FASTA_DIR      := fasta
GFF_DIR        := gff
SRA_META_DIR   := SRA_metadata
NCBI_META_DIR  := NCBI_metadata
FASTP_DIR      := fastp_metrics
BAM_DIR  := alignments
 
# Derived: last path component (full nomenclature: GCA_027936885.1_ASM2793688v1)
NCBI_PREFIX := $(notdir $(NCBI_FTP_URL))
 
# Derived: read files (must come after FASTQ_DIR is defined)
RAW_R1     := $(FASTQ_DIR)/$(ASSEMBLY_NAME)_R1.fastq
RAW_R2     := $(FASTQ_DIR)/$(ASSEMBLY_NAME)_R2.fastq
TRIMMED_R1 := $(FASTQ_DIR)/$(ASSEMBLY_NAME)_trimmed_R1.fastq
TRIMMED_R2 := $(FASTQ_DIR)/$(ASSEMBLY_NAME)_trimmed_R2.fastq

# Derived: files for alignment
REFERENCE  := $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna
BAM   := $(BAM_DIR)/$(ASSEMBLY_NAME).bam


################################################################
 
# Running the makefile
.PHONY: all dirs genome sra trim align clean
 
all: genome sra trim align
 
# Prep directories
dirs:
	mkdir -p $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) $(BAM_DIR)
 
# Download genome assembly (FASTA + GFF) and NCBI metadata
genome: dirs
	curl -fL -o $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna.gz $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.fna.gz
	curl -fL -o $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff.gz   $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.gff.gz
	gunzip -f $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna.gz $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff.gz
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_README.txt          $(NCBI_FTP_URL)/README.txt
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_assembly_report.txt $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_report.txt
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_assembly_stats.txt  $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_stats.txt
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_md5checksums.txt    $(NCBI_FTP_URL)/md5checksums.txt
 
# Download the first N reads from SRA, rename them to the sample name, and save read stats + SRA metadata
sra: dirs
	fastq-dump -X $(N) --outdir $(FASTQ_DIR) --split-files $(SRA_ACCESSION)
	mv $(FASTQ_DIR)/$(SRA_ACCESSION)_1.fastq $(RAW_R1)
	mv $(FASTQ_DIR)/$(SRA_ACCESSION)_2.fastq $(RAW_R2)
	seqkit stats $(RAW_R1) $(RAW_R2) > $(SRA_META_DIR)/$(ASSEMBLY_NAME)_seqkit_stats.txt
	bio search $(SRA_ACCESSION) | tee $(SRA_META_DIR)/$(SRA_ACCESSION)_metadata.json
 
# Trim adapters and poor-quality tails from the raw reads
trim: sra
	fastp --adapter_sequence=$(ADAPTER) \
	      --cut_tail \
	      -i $(RAW_R1) \
	      -I $(RAW_R2) \
	      -o $(TRIMMED_R1) \
	      -O $(TRIMMED_R2) \
	      --html $(FASTP_DIR)/$(ASSEMBLY_NAME)_fastp.html \
	      --json $(FASTP_DIR)/$(ASSEMBLY_NAME)_fastp.json

# Align the paired trimmed reads to the reference and save a sorted BAM.
# The pipefail setting makes a BWA failure visible instead of hiding it behind samtools.
index: genome
	bwa index $(REFERENCE)

align: index trim
	bwa mem -t 6 $(REFERENCE) $(TRIMMED_R1) $(TRIMMED_R2) | samtools sort -@ 6 -o $(BAM)
	samtools index $(BAM)
# Save alignment statistcis & print it using tee
	samtools flagstat $(BAM) | tee $(BAM_DIR)/$(ASSEMBLY_NAME)_flagstat.txt
# Print coverage plot 
	samtools coverage -A -m $(BAM)


# Remove all downloaded data
clean:
	rm -rf $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) $(BAM_DIR)
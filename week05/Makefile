SHELL := /bin/bash

# Input variables
ASSEMBLY_NAME ?= ILTV-63140
ASSEMBLY_ACCESSION ?= GCA_027936885.1
NCBI_FTP_URL ?= https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/027/936/885/GCA_027936885.1_ASM2793688v1
SRA_ACCESSION ?= SRR29869142
# N represents the number of reads for ~10x coverage
N ?= 30000
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA

# Derived: last path component, e.g. GCA_027936885.1_ASM2793688v1
NCBI_PREFIX  := $(notdir $(NCBI_FTP_URL))

# Output directories
FASTQ_DIR      := fastq
FASTA_DIR      := fasta
GFF_DIR        := gff
SRA_META_DIR   := SRA_metadata
NCBI_META_DIR  := NCBI_metadata


#Running the makefile
.PHONY: all dirs download_genome ncbi_metadata

all: download_genome ncbi_metadata

# Prep directories
dirs:
	mkdir -p $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) $(SRA_META_DIR) $(NCBI_META_DIR)

download_genome: dirs
	curl -fL -o $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna.gz $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.fna.gz
	curl -fL -o $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff.gz   $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.gff.gz
	gunzip -f $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna.gz $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff.gz

ncbi_metadata: dirs
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_README.txt          $(NCBI_FTP_URL)/README.txt
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_assembly_report.txt $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_report.txt
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_assembly_stats.txt  $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_stats.txt
	curl -fL -o $(NCBI_META_DIR)/$(ASSEMBLY_ACCESSION)_md5checksums.txt    $(NCBI_FTP_URL)/md5checksums.txt


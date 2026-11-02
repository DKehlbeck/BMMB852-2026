SHELL := /bin/bash

# Running make should default to make info, requiuring make all or make batch to execute
.DEFAULT_GOAL := info

##############################################################################
# INPUT PARAMETERS
##############################################################################
N       ?= 500000
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
THREADS ?= 4

##############################################################################
# SINGLE-SAMPLE DEFAULTS
##############################################################################
SRR 		= SRR34935931
#SRR         = SRR34326947 # Alternative set of reads for KOS
SAMPLE_NAME = KOS

##############################################################################
# REFERENCE
##############################################################################
REF_ACCESSION := GCA_027935665.1
NCBI_FTP_URL       = https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/027/935/665/GCA_027935665.1_ASM2793566v1
NCBI_PREFIX        = $(notdir $(patsubst %/,%,$(NCBI_FTP_URL)))

GENOME_FASTA = $(FASTA_DIR)/$(REF_ACCESSION).fna
GFF          = $(GFF_DIR)/$(REF_ACCESSION).gff
INDEX        = $(GENOME_FASTA).bwt

##############################################################################
# DIRECTORIES
##############################################################################
FASTQ_DIR     := fastq
FASTA_DIR     := fasta
GFF_DIR       := gff
SRA_META_DIR  := SRA_metadata
NCBI_META_DIR := NCBI_metadata
FASTP_DIR     := fastp_metrics
BAM_DIR       := alignments
VCF_DIR       := vcf
PEAKS_DIR     := peaks
BW_DIR        := bigwig

##############################################################################
# SCRIPTS / INPUT FILES
##############################################################################
PARSE_SCRIPT := parse_accessions.py
DESIGN_FILE  := design.csv
 
##############################################################################
# DERIVED SAMPLE PATHS
# NAME is resolved from the .name sidecar when SAMPLE_NAME is not set.
##############################################################################
INPUT_BAM    = $(BAM_DIR)/Input_chromatin_control.bam
MOCK_BAM     = $(BAM_DIR)/PolII_ChIPSeq_mock.bam
INFECTED_BAM = $(BAM_DIR)/PolII_ChIPSeq_HSV1_KOS.bam
FASTQ_1 = $(FASTQ_DIR)/$(SRR)_1.fastq
BAM     = $(BAM_DIR)/$(SAMPLE_NAME).bam
VCF     = $(VCF_DIR)/$(SAMPLE_NAME).vcf.gz
 
##############################################################################
# BCFTOOLS FLAGS
##############################################################################
ANN  = -d 500 --annotate 'FORMAT/DP,FORMAT/AD,FORMAT/ADF,FORMAT/ADR'
CALL = --ploidy 1 --annotate 'FORMAT/GQ'

##############################################################################
# MACS3 peak filtering/calling FLAGS
##############################################################################
MACS3_GENOME_SIZE 	= 165101
MACS3_FLAGS       	= --nomodel --broad -g $(MACS3_GENOME_SIZE)
MOCK_NAME			= Mock_infected
INFECTED_NAME		= HSV1_KOS_infected
 
##############################################################################
# BATCH
##############################################################################
DESIGN   = design.csv
PARALLEL = parallel --colsep , --header : --eta --lb -j 4

#####################################################################################################################################################################
# Code below
#####################################################################################################################################################################

##############################################################################
# Default info target for information on running makefile
##############################################################################

info:
	@echo ""
	@echo "============================================================"
	@echo "  HSV1 Read Based Variant Calling Pipeline"
	@echo "============================================================"
	@echo "  Usage:"
	@echo "    make info                              Show this message"
	@echo "    make all                               Run default sample"
	@echo "    make all SRR=SRR123 SAMPLE_NAME=Foo   Run any single sample"
	@echo "    make batch                             Run all rows in $(DESIGN)"
	@echo "    make merge                             Merge all bam/*.bam + vcf/*.vcf.gz"
	@echo "    make clean                             Remove generated outputs"
	@echo ""
	@echo "  Pipeline stages:"
	@echo "    1. genome  — download reference FASTA, GFF, and NCBI metadata"
	@echo "    2. index   — BWA + samtools index the reference"
	@echo "    3. fastq   — download reads from SRA"
	@echo "    4. align   — align, sort, and index BAM"
	@echo "    5. call    — per-sample bcftools mpileup | call"
	@echo "    6. merge   — simultaneous multi-sample VCF across all BAMs"
	@echo ""
	@echo "  Reference"
	@echo "    Accession : $(REF_ACCESSION)"
	@echo "    FASTA     : $(GENOME_FASTA)"
	@echo "    GFF       : $(GFF)"
	@echo ""
	@echo "  Sample (current)"
	@echo "    SRR         : $(SRR)"
	@echo "    SAMPLE_NAME : $(SAMPLE_NAME)"
	@echo "    N reads     : $(N)"
	@echo "    BAM         : $(BAM)"
	@echo "    VCF         : $(VCF)"
	@echo ""
	@echo "  Parameters"
	@echo "    THREADS : $(THREADS)"
	@echo "    ADAPTER : $(ADAPTER)"
	@echo "============================================================"
	@echo ""
 

##############################################################################
# STEP 0 — directories
##############################################################################
dirs:
	mkdir -p $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) \
	         $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) \
	         $(BAM_DIR) $(VCF_DIR) $(BAM_DIR) $(PEAKS_DIR) $(BW_DIR)
 
##############################################################################
# STEP 1 — download reference FASTA, GFF, and NCBI metadata via curl
##############################################################################
genome: dirs $(GENOME_FASTA)
 
$(GENOME_FASTA):
	curl -fL -o $(FASTA_DIR)/$(REF_ACCESSION).fna.gz \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.fna.gz
	curl -fL -o $(GFF_DIR)/$(REF_ACCESSION).gff.gz \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.gff.gz
	gunzip -f $(FASTA_DIR)/$(REF_ACCESSION).fna.gz \
	           $(GFF_DIR)/$(REF_ACCESSION).gff.gz
	curl -fL -o $(NCBI_META_DIR)/$(REF_ACCESSION)_README.txt \
	    $(NCBI_FTP_URL)/README.txt
	curl -fL -o $(NCBI_META_DIR)/$(REF_ACCESSION)_assembly_report.txt \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_report.txt
	curl -fL -o $(NCBI_META_DIR)/$(REF_ACCESSION)_assembly_stats.txt \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_stats.txt
	curl -fL -o $(NCBI_META_DIR)/$(REF_ACCESSION)_md5checksums.txt \
	    $(NCBI_FTP_URL)/md5checksums.txt
	seqkit stats $(GENOME_FASTA)
 
##############################################################################
# STEP 2 — index the reference
##############################################################################
index: $(INDEX)
 
$(INDEX): $(GENOME_FASTA)
	bwa index $<
	samtools faidx $(GENOME_FASTA)
 
##############################################################################
# STEP 3 — download reads
##############################################################################
fastq: $(FASTQ_1) 
 
$(FASTQ_1) :
	mkdir -p $(FASTQ_DIR)
	fastq-dump -X $(N) --split-files -O $(FASTQ_DIR) $(SRR)
	seqkit stats $(FASTQ_1) 
	bio search $(SRR) | tee $(SRA_META_DIR)/$(SRR)_metadata.json
 
##############################################################################
# STEP 4 — align
##############################################################################
align: $(BAM)
 
$(BAM): $(INDEX) $(FASTQ_1) 
	mkdir -p $(BAM_DIR)
	bwa mem -t $(THREADS) \
	    -R "@RG\tID:$(SAMPLE_NAME)\tSM:$(SAMPLE_NAME)\tPL:ILLUMINA" \
	    $(GENOME_FASTA) $(FASTQ_1)  \
	    | samtools sort -@ $(THREADS) -o $@
	samtools index $@
	samtools flagstat $@ | tee $(BAM_DIR)/$(SAMPLE_NAME)_flagstat.txt



##############################################################################
# STEP 5a — peak calling: mock vs input
# -t = treatment (mock ChIP), -c = control (input chromatin)
##############################################################################
MOCK_PEAKS = $(PEAKS_DIR)/$(MOCK_NAME)_peaks.broadPeak

$(MOCK_PEAKS): $(MOCK_BAM) $(INPUT_BAM)
	mkdir -p $(PEAKS_DIR)
	macs3 callpeak \
	    -t $(MOCK_BAM) \
	    -c $(INPUT_BAM) \
	    -n $(MOCK_NAME) \
	    --outdir $(PEAKS_DIR)
	wc -l $(MOCK_PEAKS)

##############################################################################
# STEP 5b — peak calling: infected vs input
##############################################################################
INFECTED_PEAKS = $(PEAKS_DIR)/$(INFECTED_NAME)_peaks.broadPeak

$(INFECTED_PEAKS): $(INFECTED_BAM) $(INPUT_BAM)
	mkdir -p $(PEAKS_DIR)
	macs3 callpeak \
	    -t $(INFECTED_BAM) \
	    -c $(INPUT_BAM) \
	    -n $(INFECTED_NAME) \
	    --outdir $(PEAKS_DIR)
	wc -l $(INFECTED_PEAKS)

peaks: $(MOCK_PEAKS) $(INFECTED_PEAKS)

##############################################################################
# STEP 6 — bigWig coverage tracks for IGV visualization
# bamCoverage from deeptools normalizes by sequencing depth (RPKM)
##############################################################################
coverage: \
    $(BW_DIR)/$(INPUT_NAME).bw \
    $(BW_DIR)/$(MOCK_NAME).bw \
    $(BW_DIR)/$(INFECTED_NAME).bw

$(BW_DIR)/%.bw: $(BAM_DIR)/%.bam
	mkdir -p $(BW_DIR)
	bamCoverage --binSize 1 \
	    --normalizeUsing RPKM \
	    -p $(THREADS) \
	    -b $< \
	    -o $@


##############################################################################
# STEP 5 — per-sample variant calling
##############################################################################
call: $(VCF)
 
$(VCF): $(BAM) $(GENOME_FASTA)
	mkdir -p $(VCF_DIR)
	bcftools mpileup $(ANN) -O u -f $(GENOME_FASTA) $(BAM) | \
	    bcftools call $(CALL) -mv -O u | \
	    bcftools norm -f $(GENOME_FASTA) -d all -O u | \
	    bcftools sort --write-index -O z -o $(VCF)
 
##############################################################################
# TOP-LEVEL ENTRY POINTS
##############################################################################
 
# Single sample — genome downloaded once, skipped if already present.
# Default: Peru-1. Override: make all SRR=X SAMPLE_NAME=Y
all: genome index
	$(MAKE) fastq align SRR=$(INPUT_SRR)   SAMPLE_NAME=$(INPUT_NAME)
	$(MAKE) fastq align SRR=$(MOCK_SRR)    SAMPLE_NAME=$(MOCK_NAME)
	$(MAKE) fastq align SRR=$(INFECTED_SRR) SAMPLE_NAME=$(INFECTED_NAME)
	$(MAKE) peaks
	$(MAKE) coverage 
# Batch — reference built first (skipped if present), then fastq/align/call
# runs for every row in design.csv in parallel.
# CSV must have header: SRRAccession,SampleName (spaces replaced with _ beforehand)
batch: genome index
	cat $(DESIGN) | $(PARALLEL) $(MAKE) \
	    SRR={SRRAccession} \
	    SAMPLE_NAME={LibraryName} \
	    fastq align
	$(MAKE) peaks
	$(MAKE) coverage
 
# Merge — run manually once all samples are complete.
# Produces merged-VCF.vcf.gz (bcftools merge) and merged-BAM.vcf.gz (mpileup).
merge:
	bcftools mpileup $(ANN) -O u -f $(GENOME_FASTA) $(BAM_DIR)/*.bam | \
	    bcftools call $(CALL) -mv -O u | \
	    bcftools norm -f $(GENOME_FASTA) -d all -O u | \
	    bcftools sort --write-index -O z -o $(VCF_DIR)/merged.vcf.gz
 
##############################################################################
# CLEAN
##############################################################################
clean:
	rm -rf $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) \
	       $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) \
	       $(BAM_DIR) $(VCF_DIR) \
		   $(PEAKS_DIR) $(BW_DIR)
 
.PHONY: info all dirs genome index fastq align call batch merge clean

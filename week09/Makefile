SHELL := /bin/bash
.DEFAULT_GOAL := info

##############################################################################
# INPUT PARAMETERS
##############################################################################
N       ?= 500000
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
THREADS ?= 4

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

##############################################################################
# SCRIPTS / INPUT FILES
##############################################################################
PARSE_SCRIPT := parse_accessions.py
DESIGN_FILE  := design.tsv
SRR_TSV      := SRR_accessions.tsv
REF_URL_FILE := ref_url.txt

##############################################################################
# REFERENCE
# Accession comes from design.tsv at parse time (pure awk, no network).
# FTP URL and assembly prefix are read from ref_url.txt inside recipes only,
# so Make never calls basename on an empty string.
##############################################################################
REF_ACCESSION := $(shell awk -F',' '{gsub(/ /,""); if($$2=="reference") print $$1}' $(DESIGN_FILE))
REFERENCE     := $(FASTA_DIR)/$(REF_ACCESSION).fna
GFF_FILE      := $(GFF_DIR)/$(REF_ACCESSION).gff

##############################################################################
# SAMPLES
# Read from SRR_accessions.tsv if it already exists; empty on a clean checkout
# (Make will build the TSV before it needs the values for file targets).
# Columns: SRR_Accession <tab> Name <tab> Source
# Normalize spaces and slashes in names so each sample is one safe target word.
##############################################################################
SAMPLES  := $(shell test -f $(SRR_TSV) && tail -n +2 $(SRR_TSV) | awk -F'\t' '{name=$$2; gsub(/[[:space:]]+/,"_",name); gsub(/\//,"_",name); print name}')

$(foreach row,$(shell test -f $(SRR_TSV) && tail -n +2 $(SRR_TSV) | awk -F'\t' '{name=$$2; gsub(/[[:space:]]+/,"_",name); gsub(/\//,"_",name); print $$1":"name}'),\
  $(eval SRR_$(word 2,$(subst :, ,$(row))) := $(word 1,$(subst :, ,$(row)))))

##############################################################################
# DERIVED FILE LISTS  (empty until SRR_TSV exists — that is fine)
##############################################################################
ALL_BAMS   := $(foreach s,$(SAMPLES),$(BAM_DIR)/$(s).bam)
ALL_VCFS   := $(foreach s,$(SAMPLES),$(VCF_DIR)/$(s).vcf.gz)
MERGED_VCF := $(VCF_DIR)/merged.vcf.gz

# bcftools flags
ANN  := -d 500 --annotate FORMAT/DP,FORMAT/AD,FORMAT/ADF,FORMAT/ADR
CALL := --ploidy 1 -m --keep-alts --annotate FORMAT/GQ

##############################################################################
# TOP-LEVEL PHONY TARGETS
##############################################################################
.PHONY: all info dirs accessions genome index samples merge clean cleanall

# Default behavior: typing `make` shows usage and explains the pipeline.
# Use `make all` to run the complete analysis workflow.
info:
	@echo ""
	@echo "============================================================"
	@echo "  ILTV Multi-sample Variant Calling Pipeline"
	@echo "============================================================"
	@echo "  Usage:"
	@echo "    make info      Show this help message and execution guide"
	@echo "    make all       Run the full workflow"
	@echo "    make dirs      Create required output directories"
	@echo "    make accessions Parse design.tsv into SRR_accessions.tsv and ref_url.txt"
	@echo "    make genome    Download the reference FASTA, GFF, and assembly report"
	@echo "    make index     Index the reference genome for alignment"
	@echo "    make samples   Download, trim, align, and call variants for each sample"
	@echo "    make merge     Merge all per-sample VCFs into one multi-sample VCF"
	@echo "    make clean     Remove generated analysis outputs"
	@echo "    make cleanall  Remove generated outputs and accession metadata"
	@echo ""
	@echo "  Pipeline stages:"
	@echo "    1. accessions: reads design.tsv and creates SRR_accessions.tsv + ref_url.txt"
	@echo "    2. genome: downloads the reference assembly FASTA/GFF and metadata"
	@echo "    3. index: creates BWA and samtools indices for the reference genome"
	@echo "    4. samples: for each SRR sample, downloads reads, trims adapters, aligns,"
	@echo "       calls variants, and writes per-sample VCFs"
	@echo "    5. merge: combines all sample VCFs into a single merged VCF"
	@echo ""
	@echo "  Required inputs:"
	@echo "    - design.tsv with columns: Accession, type"
	@echo "      Example: GCF_008787145.1,reference"
	@echo "      Example: SRR8282614,sample"
	@echo "    - N: reads per sample (default: $(N))"
	@echo "    - ADAPTER: trimming adapter sequence (default: $(ADAPTER))"
	@echo "    - THREADS: alignment/variant calling threads (default: $(THREADS))"
	@echo ""
	@echo "  Reference"
	@echo "    Accession : $(REF_ACCESSION)"
	@echo "    FASTA     : $(REFERENCE)"
	@echo "    GFF       : $(GFF_FILE)"
	@echo "    FTP URL   : $(shell test -f $(REF_URL_FILE) && cat $(REF_URL_FILE) || echo '(run make accessions first)')"
	@echo ""
	@echo "  Samples"
	@$(foreach s,$(SAMPLES), echo "    $(s) : $(SRR_$(s))";)
	@echo ""
	@echo "  Parameters"
	@echo "    Reads per sample (N) : $(N)"
	@echo "    Adapter              : $(ADAPTER)"
	@echo "    Threads              : $(THREADS)"
	@echo ""
	@echo "  To run the full pipeline: make all"
	@echo "============================================================"
	@echo ""

# Full pipeline entry point. This runs in two phases so the accessions file
# is generated before sample-specific file lists are expanded.
all:
	@$(MAKE) dirs accessions
	@$(MAKE) genome index samples merge
	@echo "Pipeline complete. Output files are in the generated analysis directories."

##############################################################################
# STEP 0 — directories
##############################################################################
dirs:
	mkdir -p $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) \
	         $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) \
	         $(BAM_DIR) $(VCF_DIR)

##############################################################################
# STEP 1 — parse design.tsv → SRR_accessions.tsv + ref_url.txt
##############################################################################
$(SRR_TSV) $(REF_URL_FILE): $(DESIGN_FILE) $(PARSE_SCRIPT)
	python3 $(PARSE_SCRIPT) $(DESIGN_FILE)

accessions: $(SRR_TSV)

##############################################################################
# STEP 2 — download reference FASTA + GFF
##############################################################################
$(REFERENCE): $(REF_URL_FILE)
	$(eval _FTP := $(shell cat $(REF_URL_FILE)))
	$(eval _PFX := $(shell basename $(_FTP)))
	curl -fL -o $@.gz $(_FTP)/$(_PFX)_genomic.fna.gz
	gunzip -f $@.gz

$(GFF_FILE): $(REF_URL_FILE)
	$(eval _FTP := $(shell cat $(REF_URL_FILE)))
	$(eval _PFX := $(shell basename $(_FTP)))
	curl -fL -o $@.gz $(_FTP)/$(_PFX)_genomic.gff.gz
	gunzip -f $@.gz

$(NCBI_META_DIR)/assembly_report.txt: $(REF_URL_FILE)
	$(eval _FTP := $(shell cat $(REF_URL_FILE)))
	$(eval _PFX := $(shell basename $(_FTP)))
	curl -fL -o $@ $(_FTP)/$(_PFX)_assembly_report.txt

genome: $(REFERENCE) $(GFF_FILE) $(NCBI_META_DIR)/assembly_report.txt

##############################################################################
# STEP 3 — index the reference
##############################################################################
$(REFERENCE).bwt: $(REFERENCE)
	bwa index $(REFERENCE)

$(REFERENCE).fai: $(REFERENCE)
	samtools faidx $(REFERENCE)

index: $(REFERENCE).bwt $(REFERENCE).fai

##############################################################################
# STEP 4 — per-sample: download → trim → align → per-sample VCF
# Each BAM is a proper file target so Make tracks completion correctly.
# SRA Toolkit names paired reads *_1.fastq/*_2.fastq and may name single-end
# reads either *.fastq or *_1.fastq; detect the output before processing.
##############################################################################
define SAMPLE_RULE
$(BAM_DIR)/$(1).bam: $(REFERENCE).bwt $(REFERENCE).fai
	@set -e; \
	fastq-dump -X $(N) --outdir $(FASTQ_DIR) --split-files $(SRR_$(1)); \
	if [ -f $(FASTQ_DIR)/$(SRR_$(1))_1.fastq ]; then \
		mv $(FASTQ_DIR)/$(SRR_$(1))_1.fastq $(FASTQ_DIR)/$(1)_R1.fastq; \
	elif [ -f $(FASTQ_DIR)/$(SRR_$(1)).fastq ]; then \
		mv $(FASTQ_DIR)/$(SRR_$(1)).fastq $(FASTQ_DIR)/$(1)_R1.fastq; \
	else \
		echo "ERROR: fastq-dump produced no recognized read file for $(SRR_$(1))" >&2; \
		exit 1; \
	fi; \
	if [ -f $(FASTQ_DIR)/$(SRR_$(1))_2.fastq ]; then \
		mv $(FASTQ_DIR)/$(SRR_$(1))_2.fastq $(FASTQ_DIR)/$(1)_R2.fastq; \
		fastp \
		    --adapter_sequence=$(ADAPTER) --cut_tail \
		    -i $(FASTQ_DIR)/$(1)_R1.fastq \
		    -I $(FASTQ_DIR)/$(1)_R2.fastq \
		    -o $(FASTQ_DIR)/$(1)_trimmed_R1.fastq \
		    -O $(FASTQ_DIR)/$(1)_trimmed_R2.fastq \
		    --html $(FASTP_DIR)/$(1)_fastp.html \
		    --json $(FASTP_DIR)/$(1)_fastp.json; \
		bwa mem -t $(THREADS) \
		    -R "@RG\tID:$(1)\tSM:$(1)\tPL:ILLUMINA" \
		    $(REFERENCE) \
		    $(FASTQ_DIR)/$(1)_trimmed_R1.fastq \
		    $(FASTQ_DIR)/$(1)_trimmed_R2.fastq \
		    | samtools sort -@ $(THREADS) -o $$@; \
	else \
		fastp \
		    --adapter_sequence=$(ADAPTER) --cut_tail \
		    -i $(FASTQ_DIR)/$(1)_R1.fastq \
		    -o $(FASTQ_DIR)/$(1)_trimmed_R1.fastq \
		    --html $(FASTP_DIR)/$(1)_fastp.html \
		    --json $(FASTP_DIR)/$(1)_fastp.json; \
		bwa mem -t $(THREADS) \
		    -R "@RG\tID:$(1)\tSM:$(1)\tPL:ILLUMINA" \
		    $(REFERENCE) \
		    $(FASTQ_DIR)/$(1)_trimmed_R1.fastq \
		    | samtools sort -@ $(THREADS) -o $$@; \
	fi; \
	samtools index $$@; \
	samtools flagstat $$@ | tee $(BAM_DIR)/$(1)_flagstat.txt

$(VCF_DIR)/$(1).vcf.gz: $(BAM_DIR)/$(1).bam
	bcftools mpileup \
	    --threads $(THREADS) \
	    --fasta-ref $(REFERENCE) \
	    --min-BQ 20 \
	    $(ANN) \
	    --output-type u \
	    $$< | \
	bcftools call \
	    --threads $(THREADS) \
	    --output-type z \
	    --output $$@ \
	    $(CALL)
	tabix -p vcf $$@
endef

$(foreach s,$(SAMPLES),$(eval $(call SAMPLE_RULE,$(s))))

samples: $(ALL_BAMS) $(ALL_VCFS)

##############################################################################
# STEP 5 — multi-sample merged VCF across all BAMs
##############################################################################
$(MERGED_VCF): $(ALL_BAMS)
	bcftools mpileup \
	    --threads $(THREADS) \
	    --fasta-ref $(REFERENCE) \
	    --min-BQ 20 \
	    $(ANN) \
	    --output-type u \
	    $(ALL_BAMS) | \
	bcftools call \
	    --threads $(THREADS) \
	    --output-type z \
	    --output $@ \
	    $(CALL)
	tabix -p vcf $@
	bcftools stats $@ | tee $(VCF_DIR)/merged_bcftools_stats.txt

merge: $(MERGED_VCF)

##############################################################################
# CLEAN
##############################################################################
clean:
	rm -rf $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) \
	       $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) \
	       $(BAM_DIR) $(VCF_DIR) \
		   SRR_accessions.tsv ref_url.txt

cleanall: clean
	rm -f $(SRR_TSV) $(REF_URL_FILE)

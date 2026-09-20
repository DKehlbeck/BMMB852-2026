SHELL := /bin/bash

# Dependency check
REQUIRED_TOOLS := fastq-dump seqkit fastqc fastp multiqc

# User-configurable variables
SRA_ACCESSION ?= SRR29869142
ASSEMBLY_NAME ?= ILTV-63140
N ?= 30000
# Illumina adapter sequence used during library preparation
ADAPTER ?= AGATCGGAAGAGCACACGTCTGAACTCCAGTCA

RAW_R1 := fastq/$(ASSEMBLY_NAME)_R1.fastq
RAW_R2 := fastq/$(ASSEMBLY_NAME)_R2.fastq
TRIMMED_R1 := fastq/$(ASSEMBLY_NAME)_trimmed_R1.fastq
TRIMMED_R2 := fastq/$(ASSEMBLY_NAME)_trimmed_R2.fastq

.PHONY: all check-deps metadata download raw_qc trim trimmed_qc multiqc print_tree clean

all: check-deps metadata download raw_qc trim trimmed_qc multiqc print_tree

check-deps:
	@echo "Checking dependencies..."
	@for tool in $(REQUIRED_TOOLS); do \
		if ! command -v $$tool >/dev/null 2>&1; then \
			echo "ERROR: $$tool not found."; \
			echo "Make sure it is added to your Pixi environment."; \
			exit 1; \
		else \
			echo "  OK: $$tool"; \
		fi; \
	done
	@echo "All dependencies found."


metadata:
	@echo "## Metadata for $(SRA_ACCESSION)"
	bio search $(SRA_ACCESSION)

# Download the first N reads from SRA, save them in fastq/, and rename them to a descriptive sample name.
download: $(RAW_R1) $(RAW_R2)

$(RAW_R1) $(RAW_R2):
	mkdir -p fastq
	fastq-dump -X $(N) --outdir fastq --split-files $(SRA_ACCESSION)
	@if [ -f "fastq/$(SRA_ACCESSION)_1.fastq" ]; then mv "fastq/$(SRA_ACCESSION)_1.fastq" "$(RAW_R1)"; fi
	@if [ -f "fastq/$(SRA_ACCESSION)_2.fastq" ]; then mv "fastq/$(SRA_ACCESSION)_2.fastq" "$(RAW_R2)"; fi
	@seqkit stats $(RAW_R1) $(RAW_R2) > fastq/$(ASSEMBLY_NAME)_seqkit_stats.txt

# Run FASTQC on raw reads before trimming.
raw_qc: $(RAW_R1) $(RAW_R2)
	mkdir -p fastqc_metrics
	fastqc -o fastqc_metrics $(RAW_R1) $(RAW_R2)

# Trim adapters and poor-quality tails from the raw reads.
trim: $(TRIMMED_R1) $(TRIMMED_R2)

$(TRIMMED_R1) $(TRIMMED_R2): $(RAW_R1) $(RAW_R2)
	fastp --adapter_sequence=$(ADAPTER) \
	      --cut_tail \
	      -i $(RAW_R1) \
	      -I $(RAW_R2) \
	      -o $(TRIMMED_R1) \
	      -O $(TRIMMED_R2)

# Run FASTQC on trimmed reads to assess whether QC made a difference.
trimmed_qc: $(TRIMMED_R1) $(TRIMMED_R2)
	mkdir -p fastqc_metrics
	fastqc -o fastqc_metrics $(TRIMMED_R1) $(TRIMMED_R2)

# Aggregate all FASTQC reports into one MultiQC output.
multiqc: trimmed_qc
	multiqc fastqc_metrics -o fastqc_metrics --force

# Print a compact file structure so it is easy to inspect the project.
print_tree:
	@echo "## Directory structure"
	@find . -maxdepth 2 -type d | sort
	@echo ""
	@find fastq -maxdepth 1 -type f | sort
	@echo ""
	@find fastqc_metrics -maxdepth 1 -type f | sort 2>/dev/null || true

clean:
	rm -rf fastq fastqc_metrics fastp*


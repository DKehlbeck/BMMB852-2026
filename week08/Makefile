SHELL := /bin/bash

##############################################################################
# REFERENCE — SA2 strain (GCF_008787145.1)
##############################################################################
ASSEMBLY_ACCESSION ?= GCF_008787145.1
NCBI_PREFIX        ?= GCF_008787145.1_ASM878714v1
NCBI_FTP_URL       ?= https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/008/787/145/$(NCBI_PREFIX)

##############################################################################
# SAMPLES — add a name here, then add its SRR_<name> line below
##############################################################################
SAMPLES := 63140 81658 Trachivax Peru-1

SRR_63140     := SRR29869142
SRR_81658     := SRR29869143
SRR_Trachivax := SRR29859430
SRR_Peru-1    := SRR8282614

##############################################################################
# SHARED PARAMETERS
##############################################################################
N       ?= 5000000
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

REFERENCE  := $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna
GFF_FILE   := $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff
ALL_BAMS   := $(foreach s,$(SAMPLES),$(BAM_DIR)/$(s).bam)
ALL_VCFS   := $(foreach s,$(SAMPLES),$(VCF_DIR)/$(s).vcf.gz)
MERGED_VCF := $(VCF_DIR)/merged.vcf.gz

# bcftools flags
ANN  := -d 500 --annotate FORMAT/DP,FORMAT/AD,FORMAT/ADF,FORMAT/ADR
CALL := --ploidy 1 -m --keep-alts --annotate FORMAT/GQ

##############################################################################
# TOP-LEVEL
##############################################################################
.PHONY: all info dirs genome index samples merge clean

# Default target — just print the summary, do not run the pipeline
# Default target — print summary only, pipeline does not run
info:
	@echo ""
	@echo "============================================================"
	@echo "  ILTV Multi-sample Variant Calling Pipeline"
	@echo "============================================================"
	@echo ""
	@echo "  Reference"
	@echo "    Accession : $(ASSEMBLY_ACCESSION)"
	@echo "    FASTA     : $(REFERENCE)"
	@echo "    GFF       : $(GFF_FILE)"
	@echo "    FTP URL   : $(NCBI_FTP_URL)"
	@echo ""
	@echo "  Samples"
	@$(foreach s,$(SAMPLES), \
	    echo "    $(s) : $(SRR_$(s))";)
	@echo ""
	@echo "  Parameters"
	@echo "    Reads per sample (N) : $(N)"
	@echo "    Adapter              : $(ADAPTER)"
	@echo "    Threads              : $(THREADS)"
	@echo ""
	@echo "  Pipeline steps"
	@echo "    1. genome  — download reference FASTA + GFF from NCBI"
	@echo "    2. index   — bwa + samtools index the reference"
	@echo "    3. samples — for each strain: download → trim → align → per-sample VCF"
	@echo "    4. merge   — simultaneous multi-sample VCF across all BAMs"
	@echo ""
	@echo "  Outputs"
	@echo "    BAMs   : $(BAM_DIR)/<sample>.bam"
	@echo "    VCFs   : $(VCF_DIR)/<sample>.vcf.gz"
	@echo "    Merged : $(MERGED_VCF)"
	@echo ""
	@echo "  To run the pipeline:  make all"
	@echo "  Override parameters:  make all N=30000 THREADS=8"
	@echo "============================================================"
	@echo ""

# Full pipeline — run with: make all
all: dirs genome index samples merge
	@echo ""
	@echo "============================================================"
	@echo "  ILTV Multi-sample Variant Calling Pipeline"
	@echo "============================================================"
	@echo ""
	@echo "  Reference"
	@echo "    Accession : $(ASSEMBLY_ACCESSION)"
	@echo "    FASTA     : $(REFERENCE)"
	@echo "    GFF       : $(GFF_FILE)"
	@echo "    FTP URL   : $(NCBI_FTP_URL)"
	@echo ""
	@echo "  Samples"
	@$(foreach s,$(SAMPLES), \
	    echo "    $(s) : $(SRR_$(s))";)
	@echo ""
	@echo "  Parameters"
	@echo "    Reads per sample (N) : $(N)"
	@echo "    Adapter              : $(ADAPTER)"
	@echo "    Threads              : $(THREADS)"
	@echo ""
	@echo "  Pipeline steps"
	@echo "    1. genome  — download reference FASTA + GFF from NCBI"
	@echo "    2. index   — bwa + samtools index the reference"
	@echo "    3. samples — for each strain: download → trim → align → per-sample VCF"
	@echo "    4. merge   — simultaneous multi-sample VCF across all BAMs"
	@echo ""
	@echo "  Outputs"
	@echo "    BAMs      : $(BAM_DIR)/<sample>.bam"
	@echo "    VCFs      : $(VCF_DIR)/<sample>.vcf.gz"
	@echo "    Merged    : $(MERGED_VCF)"
	@echo ""
	@echo "  Override any parameter on the command line, e.g.:"
	@echo "    make all N=100000 THREADS=8"
	@echo "    make samples N=30000"
	@echo "============================================================"
	@echo ""

dirs:
	mkdir -p $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) \
	         $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) \
	         $(BAM_DIR) $(VCF_DIR)

##############################################################################
# REFERENCE
##############################################################################
genome: dirs
	curl -fL -o $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna.gz \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.fna.gz
	curl -fL -o $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff.gz \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_genomic.gff.gz
	gunzip -f $(FASTA_DIR)/$(ASSEMBLY_ACCESSION).fna.gz \
	           $(GFF_DIR)/$(ASSEMBLY_ACCESSION).gff.gz
	curl -fL -o $(NCBI_META_DIR)/assembly_report.txt \
	    $(NCBI_FTP_URL)/$(NCBI_PREFIX)_assembly_report.txt

index: genome
	bwa index $(REFERENCE)
	samtools faidx $(REFERENCE)

##############################################################################
# PER-SAMPLE: download → trim → align → vcf
#   $(s)        = sample name  (e.g. 63140)
#   $(SRR_$(s)) = its SRR accession (e.g. SRR29869142)
##############################################################################
samples: index
	$(foreach s,$(SAMPLES), \
	  fastq-dump -X $(N) --outdir $(FASTQ_DIR) --split-files $(SRR_$(s)) && \
	  mv $(FASTQ_DIR)/$(SRR_$(s))_1.fastq $(FASTQ_DIR)/$(s)_R1.fastq && \
	  mv $(FASTQ_DIR)/$(SRR_$(s))_2.fastq $(FASTQ_DIR)/$(s)_R2.fastq && \
	  fastp \
	      --adapter_sequence=$(ADAPTER) --cut_tail \
	      -i $(FASTQ_DIR)/$(s)_R1.fastq \
	      -I $(FASTQ_DIR)/$(s)_R2.fastq \
	      -o $(FASTQ_DIR)/$(s)_trimmed_R1.fastq \
	      -O $(FASTQ_DIR)/$(s)_trimmed_R2.fastq \
	      --html $(FASTP_DIR)/$(s)_fastp.html \
	      --json $(FASTP_DIR)/$(s)_fastp.json && \
	  bwa mem -t $(THREADS) \
	      -R "@RG\tID:$(s)\tSM:$(s)\tPL:ILLUMINA" \
	      $(REFERENCE) \
	      $(FASTQ_DIR)/$(s)_trimmed_R1.fastq \
	      $(FASTQ_DIR)/$(s)_trimmed_R2.fastq \
	      | samtools sort -@ $(THREADS) -o $(BAM_DIR)/$(s).bam && \
	  samtools index $(BAM_DIR)/$(s).bam && \
	  samtools flagstat $(BAM_DIR)/$(s).bam | tee $(BAM_DIR)/$(s)_flagstat.txt && \
	  bcftools mpileup \
	      --threads $(THREADS) \
	      --fasta-ref $(REFERENCE) \
	      --min-BQ 20 \
	      $(ANN) \
	      --output-type u \
	      $(BAM_DIR)/$(s).bam | \
	  bcftools call \
	      --threads $(THREADS) \
	      --output-type z \
	      --output $(VCF_DIR)/$(s).vcf.gz \
	      $(CALL) && \
	  tabix -p vcf $(VCF_DIR)/$(s).vcf.gz ; \
	)

##############################################################################
# MERGE — simultaneous multi-sample calling across all BAMs
##############################################################################
merge: samples
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
	    --output $(MERGED_VCF) \
	    $(CALL)
	tabix -p vcf $(MERGED_VCF)
	bcftools stats $(MERGED_VCF) | tee $(VCF_DIR)/merged_bcftools_stats.txt

##############################################################################
# CLEAN
##############################################################################
clean:
	rm -rf $(FASTQ_DIR) $(FASTA_DIR) $(GFF_DIR) \
	       $(SRA_META_DIR) $(NCBI_META_DIR) $(FASTP_DIR) \
	       $(BAM_DIR) $(VCF_DIR)
ACCESSION := GCF_900476085.1

DOWNLOAD_DIR := downloads_$(ACCESSION)
DATA_DIR := $(DOWNLOAD_DIR)/data
GENOME_DIR := $(DATA_DIR)/$(ACCESSION)
PACKAGE := $(DOWNLOAD_DIR)/$(ACCESSION).zip

.PHONY: all download unzip organize move summary clean

all: move summary

download:
	mkdir -p "$(DOWNLOAD_DIR)"
	datasets download genome accession $(ACCESSION) \
		--include genome,gff3 \
		--filename "$(PACKAGE)"

unzip: download
	unzip -n "$(PACKAGE)" -d "$(DOWNLOAD_DIR)"
	find "$(DOWNLOAD_DIR)/ncbi_dataset" -print | tee "$(DOWNLOAD_DIR)/directory_after_unzip.txt"
	mkdir -p "$(DATA_DIR)"
	mv "$(DOWNLOAD_DIR)"/ncbi_dataset/data/* "$(DATA_DIR)/"
	rm -rf "$(DOWNLOAD_DIR)/ncbi_dataset"

organize: unzip
	mkdir -p "$(DATA_DIR)/fna"
	mkdir -p "$(DATA_DIR)/gff"

move: organize
	cp "$(GENOME_DIR)"/*.fna "$(DATA_DIR)/fna/"
	cp "$(GENOME_DIR)"/*.gff "$(DATA_DIR)/gff/"
	mv "$(DATA_DIR)"/fna/*.fna "$(DATA_DIR)/fna/$(ACCESSION).fna"
	mv "$(DATA_DIR)"/gff/*.gff "$(DATA_DIR)/gff/$(ACCESSION).gff"
	rm -rf "$(GENOME_DIR)"
	find "$(DATA_DIR)" -print | tee "$(DOWNLOAD_DIR)/directory_after_move.txt"

summary: move
	@python3 -c "import glob; bp=sum(sum(len(line.strip()) for line in open(p) if not line.startswith('>')) for p in glob.glob('$(DATA_DIR)/fna/*.fna')); chr=sum(1 for p in glob.glob('$(DATA_DIR)/fna/*.fna') for line in open(p) if line.startswith('>')); ann=sum(1 for p in glob.glob('$(DATA_DIR)/gff/*.gff') for line in open(p) if line and not line.startswith('#')); print(f'Genome size: {bp} bp'); print(f'Chromosomes: {chr}'); print(f'Annotation features: {ann}')"

clean:
	rm -rf "$(DOWNLOAD_DIR)"

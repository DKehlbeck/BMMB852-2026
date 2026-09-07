ACCESSION := GCF_900476085.1
DATA_DIR := data
GENOME_DIR := $(DATA_DIR)/$(ACCESSION)
PACKAGE = $(firstword $(wildcard *.zip))

.PHONY: all confirm download unzip organize move summary clean

all: confirm

confirm:
	@read -p "Would you like to download: $(ACCESSION)? [y/n] " answer; \
	if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ] || [ "$$answer" = "yes" ] || [ "$$answer" = "YES" ]; then \
		echo "Proceeding with download..."; \
		$(MAKE) move summary; \
	else \
		echo "Download cancelled."; \
		exit 1; \
	fi

download:
	# Downloads the genome fasta and corresponding gff3 for the given accession number
	datasets download genome accession $(ACCESSION) --include genome,gff3


unzip: download
	unzip -n "$(PACKAGE)"
	# Record downloaded directory format
	find ncbi_dataset -print | tee directory_after_unzip.txt
	mkdir -p $(DATA_DIR)
	mv ncbi_dataset/data/* $(DATA_DIR)/ # Move the contents of ncbi_dataset/data to data directory, avoids data/data nested directories
	rm -rf ncbi_dataset/data ncbi_dataset

organize: unzip
	# Setup dedicated directories for fasta & gff files
	mkdir -p $(DATA_DIR)/fna
	mkdir -p $(DATA_DIR)/gff

move: organize
	# Move the fasta & gff files to their respective directories and rename them to include the accession number
	cp $(GENOME_DIR)/*.fna $(DATA_DIR)/fna/
	cp $(GENOME_DIR)/*.gff $(DATA_DIR)/gff/
	mv $(DATA_DIR)/fna/*.fna $(DATA_DIR)/fna/$(ACCESSION).fna
	mv $(DATA_DIR)/gff/*.gff $(DATA_DIR)/gff/$(ACCESSION).gff
	rm -rf $(GENOME_DIR) 
	find $(DATA_DIR) -print | tee directory_after_move.txt

summary: move
	@python3 -c "import glob; bp=sum(sum(len(line.strip()) for line in open(p) if not line.startswith('>')) for p in glob.glob('data/fna/*.fna')); chr=sum(1 for p in glob.glob('data/fna/*.fna') for line in open(p) if line.startswith('>')); ann=sum(1 for p in glob.glob('data/gff/*.gff') for line in open(p) if line and not line.startswith('#')); print(f'Genome size: {bp} bp'); print(f'Chromosomes: {chr}'); print(f'Annotation features: {ann}')"

clean:
	rm -rf "$(DATA_DIR)" "$(PACKAGE)" md5sum.txt README.md directory_after_unzip.txt directory_after_move.txt ncbi_dataset

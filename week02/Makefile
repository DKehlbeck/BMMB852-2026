ACCESSION := GCF_900476085.1
DATA_DIR := data
GENOME_DIR := $(DATA_DIR)/$(ACCESSION)
PACKAGE = $(firstword $(wildcard *.zip))

.PHONY: all download unzip organize move clean

all: move

download:
	datasets download genome accession $(ACCESSION) --include genome,gff3


unzip: download
	unzip -n "$(PACKAGE)"
	find ncbi_dataset -print | tee directory_after_unzip.txt
	mkdir -p $(DATA_DIR)
	mv ncbi_dataset/data/* $(DATA_DIR)/
	rm -rf ncbi_dataset/data ncbi_dataset

organize: unzip
	mkdir -p $(DATA_DIR)/fna
	mkdir -p $(DATA_DIR)/gff

move: organize
	cp $(GENOME_DIR)/*.fna $(DATA_DIR)/fna/
	cp $(GENOME_DIR)/*.gff $(DATA_DIR)/gff/
	mv $(DATA_DIR)/fna/*.fna $(DATA_DIR)/fna/$(ACCESSION).fna
	mv $(DATA_DIR)/gff/*.gff $(DATA_DIR)/gff/$(ACCESSION).gff
	rm -rf $(GENOME_DIR) 
	find $(DATA_DIR) -print | tee directory_after_move.txt

clean:
	rm -rf "$(DATA_DIR)" "$(PACKAGE)" md5sum.txt README.md directory_after_unzip.txt directory_after_move.txt ncbi_dataset

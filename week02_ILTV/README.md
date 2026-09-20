# Mycoplasmoides gallisepticum genome analysis

This directory contains a small, reproducible workflow for downloading and organizing the NCBI RefSeq assembly `` for *Gallid alphaherpesvirus 1*, also reffered to as infectious laryngotracheitis virus, strain 63140/C/08/BR.

## Workflow usage

Requirements:

pixi envionment with the following installed packages:
- GNU Make
- NCBI `datasets` command-line tool
- `unzip`
- `find`
- Python 3 (used by the summary command)

From this directory, run:

```bash
make all
```

The default target runs `move`, which downloads the assembly and GFF3 annotation, unpacks the NCBI data package, creates the organized `data/fna/` and `data/gff/` directories, renames the files using the accession, and removes the temporary accession directory. It then runs `summary`, which prints the genome size, chromosome count, and annotation count.

Individual stages can also be run as follows:

```bash
make download   # download the NCBI Datasets package
make unzip      # unpack it into the data directory
make organize   # create fna/ and gff/ directories
make move       # copy and rename the sequence and annotation files
make summary    # calculate the three summary values
make clean      # remove the downloaded/organized package
```

If the package has already been downloaded, the workflow uses the existing files. To reproduce the complete download from scratch, run `make clean`

Original NCBI directory organization is stored in 
```bash
directory_after_unzip.txt
```

## Data organization

The data are organized by file purpose rather than placing every downloaded file in the top-level directory:

```text
week02/
├── Makefile
└── downloads_GCA_027936885.1/
    ├── data/
    │   ├── fna/GCA_027936885.1.fna    # genomic nucleotide sequence
    │   ├── gff/GCA_027936885.1.gff    # genome annotation
    │   ├── assembly_data_report.jsonl  # assembly metadata
    │   └── dataset_catalog.json        # NCBI package metadata
    ├── directory_after_unzip.txt
    ├── directory_after_move.txt
    └── md5sum.txt
```

The FASTA sequence and GFF annotation are kept in separate `fna/` and `gff/` directories. The downloaded package metadata and directory listings are retained alongside them for provenance.

## Limitations & other usage

As the genome accession is hard coded, this script may be adapted for other NCBI assembled genomes by changing line 1 for the desired genome

If a microbial genome has multiple independent fastas, such as a segmented virus, this script will not work

If any additional files outside of .fna or .gff3 are needed, those are hard coded in download and can be appended.

# Genome summary

The values below were calculated from the files in `data/fna/` and `data/gff/` by the Makefile's `summary` target.

| Question | Answer |
| --- | --- |
| How large is the genome? | **153,633 bp** |
| How many chromosomes does it have? | **1 chromosome** (`JN542536.1`) |
| How many annotation records are in the GFF file? | **162 records, including genes, CDS, and regions** |
| How many gene records are present? | **79 genes with 82 CDS** | 

3 genes have splice variants (UL-1, UL0, and UL15) which accounts for the additional 3 CDS.  

## Assembly completeness

NCBI describes it as a **Complete Genome**, and the FASTA contains one annotated chromosome sequence. Suggestive of a completely assembled genome. Inspection of gff and annotations suggest no incomplete genes/CDS.

## IGV visualization

The supplied FASTA and GFF were loaded into IGV. The GFF track displays annotated genomic features, especially genes and their corresponding CDS features; RNA transcripts/features are also shown where they are present in the annotation. Features were colored by strand orientation:

- **Blue:** forward (`+`) strand
- **Red:** reverse (`-`) strand

#### Example


![IGV view of genome positions 65kb-130kb showing reverse and forward features in the GFF track.](images/igv_overview_2026-09-20 142713.png)


### Gene packing

Most genomic features are **10–200 bp apart**, while a few are seperated by **300-4,000+. 11 Genes overlap with at least one other gene.

### Coordinate 74,960

- At chromosome position **63,540*, the inspected forward strand base is **guanine (G)** found in the gene UL36. 
- This coordinate can fall in a foward frame producing **M**, **W**, or a **G**, though this is non-coding for the gene it is located in. 
- On the reverse, coding strand for UL36, the three codon frames correspond to an  **S**, **P**, or **H**. 

![IGV view centered near chromosome position 63,540, showing the sequence, forward frame, and GFF feature track.](images/fwd_reading_frame_2026-09-20 143042.png)

![IGV view centered near chromosome position 63,540, showing the sequence, reverse frame, and GFF feature track.](images/rev_reading_frame_2026-09-20 142956.png)
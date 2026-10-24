# Automating variant calling between genomes

## Resolve SRR and BioProject accessions

Run `resolve_design.py` with SRR and/or BioProject accessions. For example:

```text
python resolve_design.py SRR8282614 PRJNA1136498 SRR29859430
```

The script looks up every run associated with each BioProject and writes
`srr_names.csv` with `SRR` and `Name` columns. You can also put the accessions
in a text file, one per line, and run:

```text
python resolve_design.py --input-file accessions.txt --output results.csv
```

The pipeline reads its input list from `design.csv` and creates a tab-separated
manifest at `SRA_metadata/resolved_samples.tsv` for downstream processing.

# Collaborating via github 

## Forking a directory

## Investigating a peers week02 genome assembly download pipeline

Inspect README & Makefile to understand how to execute and any potential issues

```bash
cat README.md && cat Makefile
```

The makefile should not make, edit, or remove any files in other directories. However, if another directory called fasta or gff is present, those will be removed if the following is executed:

```bash
make clean
```

To execute the download of Aedes albopictus genome run:

```bash
make
```

This should download the following items

Dependencies are listed in the README: samtools is requiured 

## Comparing pipelines 

AI prompt:

```bash
"Critically compare and contrast two makefiles to download a relatively small genome in preperation for viewing in a genomic viewing program such as IGV. Investigate things like: simplicity, documentation, organization, reproducibility, adaptability and any other factors deemed important or distinct between the two files. Then use those comparison criteria to determine which makefile is better for each aspect and overall."
```

Summary of comparisons:

    Overall the sampled directories makefile to download a genome assembly was executed better than my own approach. It was simpler, relied on less dependencies, and was organized equally as well. The complexities in my makefile arose from some both beneficial features and redundant ones such as relying on only a genome assembly accession number to be provided rather than a hard link to the ncbi directory. However because I am able to do this with datasets, it also makes the file downloads more convlouded and requoures addiciotnally reorganization of files into the necessary formats. The AI stated those features can aid in adaptablity, but also hinder in reproducibility. 

## Updating the forked directory

Updated applied-bioinfo-2026-AY/week02/README.md to include genome accession & NCBI link information in Makefile

[Link to git commit for update](https://github.com/DKehlbeck/applied-bioinfo-2026-AY/commit/211184d25203b81bf2c4c0fbda712ecdeebfacba)
# Collaborating via github 

## Forking a directory

Forked Ann Safo's repo

[Link to repo](https://github.com/annyaa/applied-bioinfo-2026)

```bash
# Press fork on GitHub repo link
# Navigate to week03 directory on local machine for local organization of repo
cd week03

# Clone directory onto local machine
git clone  https://github.com/DKehlbeck/applied-bioinfo-2026-AY.git

# Confirm cloned git repo is from forked directory made by DKehlbeck
git remote -v
    origin  https://github.com/DKehlbeck/applied-bioinfo-2026-AY.git (fetch)
    origin  https://github.com/DKehlbeck/applied-bioinfo-2026-AY.git (push)

# Navigate to forked repo week02 genome assembly viewer 
cd applied-bioinfo-2026-AY/week02
```

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

Output of make all:

```bash
$ make 

mkdir -p fasta
curl -L https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/035/046/485/GCF_035046485.1_AalbF5/GCF_035046485.1_AalbF5_genomic.fna.gz -o fasta/Albopictus.fna.gz
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100 403.1M 100 403.1M   0      0 23.41M      0   00:17   00:17         24.25M
gunzip -c fasta/Albopictus.fna.gz > fasta/Albopictus.fa
samtools faidx fasta/Albopictus.fa
mkdir -p gff
curl -L https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/035/046/485/GCF_035046485.1_AalbF5/GCF_035046485.1_AalbF5_genomic.gff.gz -o gff/Albopictus.gff.gz
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100  6.77M 100  6.77M   0      0  9.09M      0                              0
gunzip -c gff/Albopictus.gff.gz > gff/Albopictus.gff
(grep '^#' gff/Albopictus.gff; grep -v '^#' gff/Albopictus.gff | sort -k1,1 -k4,4n) | bgzip > gff/Albopictus.gff.gz.tmp
mv gff/Albopictus.gff.gz.tmp gff/Albopictus.gff.gz
rm -f gff/Albopictus.gff
tabix -p gff gff/Albopictus.gff.gz
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


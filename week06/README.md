# Week 6 - Inspecting BAM files for evidence of genomic changes to a reference sequence

The goal of this week was to understand how visualizing read-pair orientation can help interpret differences between sequenced reads and the reference sequence.

Specifically, the goal was to identify changes such as deletions, insertions, duplications, translocations, and inversions.

Five sample BAM files were provided for a single reference genome:

- Reference: [Ebola reference FASTA](https://data.biostarhandbook.com/courses/2026-appbio/igv/fasta/ebola-1976.fa)
- Sample 1: [Sample 1 BAM](https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_1.bam)
- Sample 2: [Sample 2 BAM](https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_2.bam)
- Sample 3: [Sample 3 BAM](https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_3.bam)
- Sample 4: [Sample 4 BAM](https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_4.bam)
- Sample 5: [Sample 5 BAM](https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_5.bam)

## Sample 1 - Reads supporting the reference

![Sample 1 reads supporting the reference](images/bam1_2026-10-04%20233637.png)

The first example appears like the reference with a few SNPs around 0.9kb, 2kb, and 14.3kb. Additionally, there are two positions were a fraction of reads support a small insertion.

## Sample 2 - Reads containing substantial variability

![Sample 2 reads containing substantial variability](images/bam2_2026-10-04%20233709.png)

The second example bam contains reads that themselves vary dramatically from the consensus sequence, as indiciated by the multi colored positions the majority of reads. However, while these appear to be highly variable within all of the reads, this variability does not appear to support differences to the reference


## Sample 3 - Coverage differences suggesting large duplications

![Sample 3 coverage differences suggesting large duplications](images/bam3_2026-10-04%20233731.png)

Immediately noticeable are three genomic loci containing ~3-4 times more coverage than the rest of the genome (~35x coverage). Though coverage alone can hint, but is less definitive. 

When we take the portion of the reads that are clipped and search for them across the genome, we see that these sequences map to the opposite end of the ~1 kb region. This may suggest reads span the boundaries between two repeating units that didn’t exist in the reference genome.


![Sample 3 repeat junction boundaries](images/bam3_repeat_junction_boundaries_annotated_2026-10-04%20233753.png)

## Sample 4 - Read-pair orientation suggesting an inversion

Example 4 shows 3 different types of pair orientation: RR, LL, LR. The expected orientation for illumina reads would be LR where paired end reads face inward ( → ←). However this is not observed for reads mapping to positions 4,550 - 6,450 where paired end reads are LL ( ← ←) or RR ( → →) suggesting a potential rearrangmenet/inversion in the sequenced sample compared to the reference. 

![Sample 4 read-pair orientation overview](images/bam4_2026-10-04%20233823.png)

Closer inspection of varied read pair orientation patterns supporting a potential inversion


![Sample 4 read-pair orientation detail](images/bam4_orientation%292026-10-04%20233843.png)

## Sample 5 - Read-pair orientation suggesting a rearrangement/translocation

Similarly this set of reads has multiple pair orientations, both expected LR, but also a RL, outward facing pairs ( ← →). This would provide evidence for a potential genomic rearrangement. In the reference genome, the upstream region is expected to contain right-facing reads (→) and the downstream region left-facing reads (←), this is not observed. A translocation involving this region could disrupt this expected orientation by bringing sequences from a different genomic location into proximity, resulting in a change in paired-end read orientation and the presence of outward-facing read pairs at some position between 5,500 & 6,500.

![Sample 5 read-pair orientation overview](images/bam5_2026-10-04%20233903.png)

Closer inspection of outward read pair orientation patterns supporting a potential translocation

![Sample 5 pair orientation detail](images/bam5_pair_orientation_2026-10-04%20233935.png)

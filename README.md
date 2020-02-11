## Introduction

This is chipseq data analysis of sample sard1. The chipseq data raw data was obtained from [NCBI](https://www.ncbi.nlm.nih.gov/sra?term=SRX1371906). There is one untreated and one treated datasets.

## Requirements

1) bowtie2 v 2.3.5
2) macs2 v2.2.6
3) python v3.6+ <3.7
4) snakemake v5.10
5) samtools v1.9


## Method

Chipseq raw reads were aligned using bowtie2 and sorted bam files were generated using samtools.

macs2 was used to callpeaks from untreated and treated data sorted bam files.

## How to run the script

Run this command in the HPC
```
source python-3.6.1
source bowtie2-2.3.5
source samtools-1.9
snakemake -s scripts/analysis.py -p chipseq
```


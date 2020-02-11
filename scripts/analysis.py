#!/usr/bin/env python3

projectdir = "/tsl/scratch/shrestha/pingtao/sard1_chipseq/"
reference = "/tsl/data/sequences/plants/arabidopsis/tair10/genome/TAIR10_genome.fa"
gff = "/tsl/data/sequences/plants/arabidopsis/tair10/annotation/Arabidopsis_thaliana.TAIR10.36.gff3"

rule sard1_extreads:
    input: "/tsl/data/extReads/{srr}.fastq.gz"
    output: projectdir + "results/alignment/{srr}_sorted.bam"
    threads: 16
    resources: mem_mb = lambda wildcards, attempt: attempt * 300000
    benchmark: projectdir + "benchmark/alignment/{srr}.txt"
    log: projectdir + "logs/alignment/{srr}.log"
    shell: "bowtie2 --threads {threads} -x {reference} --sensitive --end-to-end --maxins 20000 --time --no-unal --qc-filter -U {input}  | samtools view -b --reference {reference} --threads {threads} | samtools sort -o {output} && samtools index {output}"

rule chipseq:
    input:
        treatment = projectdir + "results/alignment/SRR2776874_sorted.bam",
        control = projectdir + "results/alignment/SRR2776875_sorted.bam"
    output:
        outfiles = [projectdir + "results/chipseq/sard1_control_lambda.bdg",
            projectdir + "results/chipseq/sard1_cutoff_analysis.txt",
            projectdir + "results/chipseq/sard1_model.r",
            projectdir + "results/chipseq/sard1_peaks.narrowPeak",
            projectdir + "results/chipseq/sard1_peaks.xls",
            projectdir + "results/chipseq/sard1_summits.bed",
            projectdir + "results/chipseq/sard1_treat_pileup.bdg"]

    message: "Chipseq analysis"
    benchmark: projectdir + "benchmark/chipseq/sard1_chipseq.log"
    log: projectdir + "logs/chipseq/sard1_chipseq.log"
    shell: "macs2 callpeak -t {input.treatment} -c {input.control} -f BAM -g 135000000 --keep-dup all --outdir {projectdir}/results/chipseq --name sard1 --bdg --verbose 2 --trackline --d-min 30 --call-summits --fe-cutoff 5 --cutoff-analysis --tsize 42 --pvalue 0.01 --min-length 10 --max-gap 10 --format BAM --scale-to large > {log} "

rule run_analysis:
    input: expand([projectdir + "results/alignment/{srr}_sorted.bam"], srr=["SRR2776874", "SRR2776875"])

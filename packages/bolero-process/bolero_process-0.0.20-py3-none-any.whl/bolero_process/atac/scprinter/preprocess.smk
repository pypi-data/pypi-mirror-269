import joblib
samples = joblib.load('ids')
# samples = ['sample1']

chrom_sizes_path = "CHROM_SIZE_PATH"
cpu = 4
mem_mb_per_cpu = 4000
picard_mem_gb = int(cpu * mem_mb_per_cpu * 0.9 / 1000)

import pysam
import sys
import subprocess
import pathlib
import numpy as np


def get_picard_jar_path():
    path = subprocess.check_output(["which", "picard"], encoding="utf8")
    jar_path = pathlib.Path(path.strip()).resolve().parent / "picard.jar"
    assert jar_path.exists(), "picard.jar not found, make sure picard is installed."
    return jar_path


def threads_to_total_mem_gb(wildcards, threads):
    mem_gb = int(np.floor(threads * mem_mb_per_cpu * 0.9 / 1000))
    return mem_gb


def add_cell_barcode_tag(input_bam_path, output_bam_path):
    input_bam_path = str(input_bam_path)
    output_bam_path = str(output_bam_path)

    # Open the input BAM file for reading and create a new BAM file for writing
    with pysam.AlignmentFile(input_bam_path, "rb") as infile, pysam.AlignmentFile(
        output_bam_path, "wb", template=infile
    ) as outfile:
        # Iterate over each read in the original BAM file
        for read in infile:
            # Extract the cell barcode (first part of the read name before the colon)
            cell_barcode = read.query_name.split(":")[0]

            # Add the CB:Z tag with the cell barcode
            read.set_tag("CB", cell_barcode, value_type="Z")
            read.set_tag("XC", cell_barcode, value_type="Z")

            # Write the modified read to the new BAM file
            outfile.write(read)


def bam_to_frag(in_path, out_path, barcode_tag="CB", shift_plus=4, shift_minus=-4):
    """
    Convert coordinate-sorted BAM file to a fragment file format, while adding Tn5 coordinate adjustment
    BAM should be pre-filtered for PCR duplicates, secondary alignments, and unpaired reads
    Output fragment file is sorted by chr, start, end, barcode
    """
    in_path = str(in_path)
    out_path = str(out_path)

    input = pysam.AlignmentFile(in_path, "rb")
    with open(out_path, "w") as out_file:
        buf = []
        curr_pos = None
        for read in input:
            if read.flag & 16 == 16:
                continue  # ignore reverse (coordinate-wise second) read in pair

            chromosome = read.reference_name
            start = read.reference_start + shift_plus
            end = read.reference_start + read.template_length + shift_minus
            cell_barcode = read.get_tag(barcode_tag)
            # assert(read.next_reference_start >= read.reference_start) ####
            data = (chromosome, start, end, cell_barcode, 1)
            pos = (chromosome, start)

            if pos == curr_pos:
                buf.append(data)
            else:
                buf.sort()
                for i in buf:
                    print(*i, sep="\t", file=out_file)
                buf.clear()
                buf.append(data)
                curr_pos = pos
    return


rule final:
    input:
        expand("cutsites/{sample}.cutsites.zarr/.success", sample=samples),
        expand("cutsites/{sample}.h5ad", sample=samples)


rule gsutil:
    output:
        temp("input_{sample}.bam"),
    threads: cpu
    shell:
        "gsutil -m cp gs://hanqing-wmb-browser/raw_bams/{wildcards.sample}.bam {output}"


rule sort_raw_bam:
    input:
        "input_{sample}.bam",
    output:
        bam=temp("bam/{sample}.sort.bam"),
        bai=temp("bam/{sample}.sort.bam.bai"),
    threads: cpu
    resources:
        mem_gb=threads_to_total_mem_gb,
        temp_prefix="bam/{sample}",
    params:
        mem_per_cpu=int(mem_mb_per_cpu * 0.9 / 1000),
        temp_prefix="bam/{sample}",
    shell:
        "samtools sort -@ {threads} -T {params.temp_prefix} -m {params.mem_per_cpu}G -o {output.bam} {input} "
        "&& sambamba index -t {threads} {output.bam}"


rule get_chroms:
    input:
        "bam/{sample}.sort.bam",
    output:
        temp("bam/{sample}.valid_chroms.txt"),
    shell:
        "samtools view -H {input} | "
        "grep chr | "
        "cut -f2 | "
        "sed 's/SN://g' | "
        "awk '{{if(length($0)<6)print}}' > "
        "{output} "


rule filter_bam:
    input:
        bam="bam/{sample}.sort.bam",
        bai="bam/{sample}.sort.bam.bai",
        chroms="bam/{sample}.valid_chroms.txt",
    output:
        bam=temp("bam/{sample}.filtered.bam"),
        bai=temp("bam/{sample}.filtered.bam.bai"),
    threads: cpu
    shell:
        "sambamba view -h -t {threads} --num-filter 2/524 -o {output.bam} -f bam {input.bam} $(cat {input.chroms})"


rule tag_barcode:
    input:
        "bam/{sample}.filtered.bam",
    output:
        temp("bam/{sample}.bctag.bam"),
    run:
        add_cell_barcode_tag(input_bam_path=input, output_bam_path=output)


rule name_sort_bam:
    input:
        "bam/{sample}.bctag.bam",
    output:
        temp("bam/{sample}.bctag_name_sort.bam"),
    threads: cpu
    resources:
        mem_gb=threads_to_total_mem_gb,
    params:
        mem_per_cpu=int(mem_mb_per_cpu * 0.9 / 1000),
        temp_prefix="bam/{sample}",
    shell:
        "samtools sort -@ {threads} -m {params.mem_per_cpu}G -T {params.temp_prefix} -n -o {output} {input} "


rule fixmate:
    input:
        "bam/{sample}.bctag_name_sort.bam",
    output:
        temp("bam/{sample}.fixmate.bam"),
    threads: cpu
    params:
        fixmate_threads=int(cpu * 2),
    shell:
        "sambamba view -t {threads} -h -f sam {input} | samtools fixmate -@ {params.fixmate_threads} -r /dev/stdin {output}"


rule mark_duplicates:
    input:
        "bam/{sample}.fixmate.bam",
    output:
        bam=temp("bam/{sample}.dedup.bam"),
        metric="bam/{sample}.mark_duplicates_metrics.txt",
    threads: cpu
    params:
        jar_path=get_picard_jar_path(),
    resources:
        mem_gb=threads_to_total_mem_gb,
    shell:
        "java -Dsamjdk.compression_level=5 "
        "-Xmx{resources.mem_gb}G "
        "-jar {params.jar_path} MarkDuplicates "
        "INPUT={input} "
        "OUTPUT={output.bam} "
        "TMP_DIR=bam/ "
        "METRICS_FILE={output.metric} "
        "VALIDATION_STRINGENCY=LENIENT "
        "ASSUME_SORT_ORDER=queryname "
        "REMOVE_DUPLICATES=false "
        "TAG_DUPLICATE_SET_MEMBERS=true "
        "READ_NAME_REGEX=NULL "
        "MAX_OPTICAL_DUPLICATE_SET_SIZE=-1 "
        "BARCODE_TAG=CB "


rule filter_dedup_bam:
    input:
        "bam/{sample}.dedup.bam",
    output:
        bam=temp("bam/{sample}.dedup_filtered.bam"),
    threads: cpu
    shell:
        "sambamba view -t {threads} -h --num-filter 2/1804 -f bam -o {output} {input}"


rule sort_dedup_bam:
    input:
        "bam/{sample}.dedup_filtered.bam",
    output:
        bam="bam/{sample}.dedup_filtered_sort.bam",
        bai="bam/{sample}.dedup_filtered_sort.bam.bai",
    threads: cpu
    resources:
        mem_gb=threads_to_total_mem_gb,
    params:
        mem_per_cpu=int(mem_mb_per_cpu * 0.9 / 1000),
        temp_prefix="bam/{sample}",
    shell:
        "samtools sort -@ {threads} -m {params.mem_per_cpu}G -T {params.temp_prefix} -o {output.bam} {input} "
        "&& sambamba index -t {threads} {output.bam}"


rule generate_fragment_file:
    input:
        "bam/{sample}.dedup_filtered_sort.bam",
    output:
        "fragments/{sample}.tsv",
    threads: 2
    run:
        bam_to_frag(input, output, barcode_tag="CB", shift_plus=4, shift_minus=-4)


rule bgzip_fragment_file:
    input:
        "fragments/{sample}.tsv",
    output:
        "fragments/{sample}.tsv.gz",
    threads: cpu
    shell:
        "bgzip -f -@ {threads} {input}"


from bolero_process.atac.sc.fragments_to_zarr import fragments_to_cutsite_zarr


rule fragments_to_zarr:
    input:
        "fragments/{sample}.tsv.gz",
    output:
        "cutsites/{sample}.cutsites.zarr/.success",
    params:
        zarr_path="cutsites/{sample}.cutsites.zarr",
    threads: 2
    resources:
        mem_gb=12
    run:
        fragments_to_cutsite_zarr(
            fragments_path=str(input),
            chrom_sizes_path=chrom_sizes_path,
            output_zarr_path=str(params.zarr_path),
            barcode_prefix=None,
            chrom_col=0,
            start_col=1,
            end_col=2,
            barcode_col=3,
            chrom2_col=None,
            end2_col=None,
            strand_col=None,
            strand2_col=None,
            mapq_col=None,
            min_mapq=30,
            format="bed",
            plus_shift=0,
            minus_shift=-1,
            chunk_size=20000000,
            sort_fragments=False,
            temp_dir="/tmp",
            remove_chr=False,
        )


import scprinter as scp
mm10 = scp.genome.Genome(
        {
            "chr1": 195471971,
            "chr2": 182113224,
            "chr3": 160039680,
            "chr4": 156508116,
            "chr5": 151834684,
            "chr6": 149736546,
            "chr7": 145441459,
            "chr8": 129401213,
            "chr9": 124595110,
            "chr10": 130694993,
            "chr11": 122082543,
            "chr12": 120129022,
            "chr13": 120421639,
            "chr14": 124902244,
            "chr15": 104043685,
            "chr16": 98207768,
            "chr17": 94987271,
            "chr18": 90702639,
            "chr19": 61431566,
            "chrX": 171031299,
            "chrY": 91744698,
        },
        "gencode_vM25_GRCm38.gff3.gz",
        "gencode_vM25_GRCm38.fa.gz",
        "mm10Tn5Bias.h5",
        "mm10-blacklist.v2.bed.gz",
        (0.29149763779592625,
         0.2083275235867118,
         0.20834346947899296,
         0.291831369138369)
    )

def run_scp(frag_path, adata_path, sample):

    printer = scp.pp.import_fragments(str(frag_path),
                                      genome=scp.genome.mm10,
                                      savename=str(adata_path),
                                      barcodes=None,
                                      plus_shift=4,
                                      minus_shift=-4,
                                      sorted_by_barcode=False,
                                      auto_detect_shift=False)
    #print('generate bigwig')
    #scp.pp.sync_footprints(printer, printer.insertion_file.obs_names, str(sample))
    return


rule fragments_to_h5ad_and_bigwig:
    input:
        "fragments/{sample}.tsv.gz",
    output:
        adata="cutsites/{sample}.h5ad"
    resources:
        mem_gb=12
    threads: 2
    run:
        run_scp(
            frag_path=input,
            adata_path=output.adata,
            sample=wildcards.sample
        )

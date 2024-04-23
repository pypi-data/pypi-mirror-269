#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   HBA2_fusion.py
@Time    :   2024/03/27 11:18:34
@Author  :   Liu.Bo
@Version :   1.0.0.0
@Contact :   liubo4@genomics.cn/614347533@qq.com
@WebSite :   http://www.ben-air.cn/
@Description :
@Notes :
@References: :
'''
from argparse import ArgumentParser
import pysam
from collections import namedtuple
import pandas as pd
import os 


program = 'HBA2_fusion.py'
version = '1.0.0.0'

Read = namedtuple('Read', ['read_name', 'pair', 'strand'])
CisTransSingle = namedtuple('site', ["chr", "site", "ref", "alt"])


def get_snv_support_reads(VcfMut, bam_file, ref, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
    support_reads = []
    cover_reads = []
    start_reads = {}
    EndSite = VcfMut.site + len(VcfMut.ref)
    for pileup_column in bam_file.pileup(region=str(VcfMut.chr) + ':' + str(VcfMut.site) + '-' + str(VcfMut.site),mapq=mapq , baseq = baseq,
                                         stepper=stepper, fastaFile=ref, max_depth=200000, **{"truncate": True}):
        if pileup_column.nsegments > 0:
            for pileup_read in pileup_column.pileups:
                aln = pileup_read.alignment
                read_name = aln.query_name
                pair = 'pe1' if aln.is_read1 else 'pe2'
                strand = '-' if aln.is_reverse else '+'
                read = Read(read_name, pair, strand)
                if pileup_read.is_del or pileup_read.is_refskip or (aln.flag > 1024) or (aln.mapping_quality < mapq) or \
                        aln.query_qualities[pileup_read.query_position] < baseq:
                    continue
                start_reads[read] = [pileup_read.query_position, aln]
    for pileup_column in bam_file.pileup(region=str(VcfMut.chr) + ':' + str(EndSite) + '-' + str(EndSite),
                                         stepper=stepper, fastaFile=ref, max_depth=200000, **{"truncate": True}):
        if pileup_column.nsegments > 0:
            for pileup_read in pileup_column.pileups:
                aln = pileup_read.alignment
                read_name = aln.query_name
                pair = 'pe1' if aln.is_read1 else 'pe2'
                strand = '-' if aln.is_reverse else '+'
                read = Read(read_name, pair, strand)
                if pileup_read.is_del or pileup_read.is_refskip:
                    continue
                if read in start_reads:
                    start_query_position, start_aln = start_reads[read]
                    seq = start_aln.query_sequence[start_query_position:pileup_read.query_position]
                    cover_reads.append(aln)
                    if seq.upper() == VcfMut.alt.upper():
                        support_reads.append(aln)
    readID_list = []
    readID2Read = {}
    cover_readID = []
    for aln in cover_reads:
        cover_readID.append(aln.query_name)
    for aln in support_reads:
        readID_list.append(aln.query_name)
        readID2Read[aln.query_name] = aln
    depth = len(cover_readID)
    support = len(readID_list)
    ratio = int(support*1000/depth)/1000
    return [readID_list,readID2Read,cover_readID,ratio]

def main():
    parser = ArgumentParser(prog=program)
    parser.add_argument('-cfg' , dest='config' , default= os.path.join(os.path.dirname(__file__),"HBA2_fusion.db"), action='store', type=str, help='input config File')
    parser.add_argument('-bam' , dest='bam_file' , required=True, action='store', type=str, help='input bam File')
    parser.add_argument('-ref' , dest='reference' , required=True, action='store', type=str, help='input reference File(In Fasta Format)')
    parser.add_argument('-genome' , dest='genome_version' , default="Hg19", action='store', type=str, help='Hg19(default) or GRCh38')
    parser.add_argument('-cut' , dest='depth_cut' , default=10, action='store', type=int, help='required depth cut')

    parser.add_argument('-out', dest='output', required=True, action='store', type=str, help='output File')

    args = parser.parse_args()
    HBA2_fusion_cfginfo = pd.read_csv(args.config, sep='\t')
    bam_pysam = pysam.AlignmentFile(args.bam_file)
    out=""
    title=""
    pos_site=0
    miss_site=0
    neg_site=0
    OUT=open(args.output, "w")
    for Mutation in HBA2_fusion_cfginfo.itertuples():
        if args.genome_version == "Hg19":
            Mut = CisTransSingle(Mutation.chrom ,Mutation.Hg19, Mutation.ref, Mutation.alt)
        elif args.genome_version == "GRCh38":
            Mut = CisTransSingle(Mutation.chrom ,Mutation.GRCh38, Mutation.ref, Mutation.alt)
        else :
            print("Please input the correct genome version")
            exit(0)
        readID_list,readID2Read,cover_readID,ratio = get_snv_support_reads(Mut, bam_pysam ,args.reference)
        if len(cover_readID)>args.depth_cut :
            if ratio>Mutation.cut:
                pos_site+=1
            else:
                neg_site+=1
            title=title+"\t"+Mutation.index
            out=out+"\t"+str(ratio)+"|"+str(len(readID_list))+"|"+str(len(cover_readID))
        else:
            miss_site+=1
            title=title+"\t"+Mutation.index
            out=out+"\t"+"NoEnoughDepth"+"|"+str(len(readID_list))+"|"+str(len(cover_readID))

    if pos_site>=4 :
        final_tag = "True"
    elif neg_site>=4:
        final_tag = "Flase"
    elif miss_site>=2:
        final_tag = "NoEnoughCoverSite"

    OUT.write("sample"+title+"\tHBA2-Fusion\n")
    OUT.write(args.bam_file+out+"\t"+final_tag+"\n")

if __name__ == '__main__':
    main()


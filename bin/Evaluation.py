from hc_common import GetBed,SplitHiconf
from indel import GetGoldINDEL,Compare_INDEL,vcfdict_INDEL
from snp import GetGoldSNP,Compare_SNP,vcfdict_SNP
from sv import GetGoldSV,Compare_SV,vcfdict_SV
from argparse import ArgumentParser
import time

parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n liuyichen@std.uestc.edu.cn\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--bed_hc','-b',help="Bed file which represents high confidence region",default=False)
parser.add_argument('--gold_gz','-g',help="Gold standard vcf file (gziped)",required=True)
parser.add_argument('--vcf_file','-v',help="Vcf file to be evaluated",required=True)
parser.add_argument('--file_out_dir','-o',help="If set, evaluate resilts will be output to the specified dir",default=False)
parser.add_argument('--snp_eval','-snp',help='If set, evaluate SNP in input vcf file (if none of snp,sv,indel flag is set, ALL of them will be evaluated)',action="store_true")
parser.add_argument('--sv_eval','-sv',help='If set, evaluate SV in input vcf file (if none of snp,sv,indel flag is set, ALL of them will be evaluated)',action="store_true")
parser.add_argument('--indel_eval','-indel',help='If set, evaluate INDEL in input vcf file (if none of snp,sv,indel flag is set, ALL of them will be evaluated)',action="store_true")
args = parser.parse_args()


if __name__ == "__main__":
    bed_file = args.bed_hc
    vcf_file = args.vcf_file
    gold_file = args.gold_gz
    
    file_out_dir = args.file_out_dir
    snp_flag = args.snp_eval
    indel_flag = args.indel_eval
    sv_flag = args.sv_eval
    all_flag = not (snp_flag or sv_flag or snp_flag)

    t = time.time()
    if bed_file:
        bed = GetBed(bed_file)

    if snp_flag or all_flag:
        print("SNP evaluation start")
        vcf_snp = vcfdict_SNP(vcf_file)
        gold_snp = GetGoldSNP(gold_file)
        if bed_file:
            SNP_vcf_HC = SplitHiconf(bed,vcf_snp)
            Gold_SNP_HC = SplitHiconf(bed,gold_snp)
            Compare_SNP(SNP_vcf_HC,Gold_SNP_HC,file_out_dir)
        else:
            Compare_SNP(vcf_snp,gold_snp,file_out_dir)
        print("SNP evaluation finished")
    
    if indel_flag or all_flag:
        print("INDEL evaluation start")
        vcf_indel = vcfdict_INDEL(vcf_file)
        INDEL_Gold_simple,INDEL_Gold_complex = GetGoldINDEL(gold_file)
        if bed_file:
            INDEL_vcf_HC = SplitHiconf(bed,vcf_indel)
            INDEL_Gold_simple_HC = SplitHiconf(bed,INDEL_Gold_simple)
            INDEL_Gold_complex_HC = SplitHiconf(bed,INDEL_Gold_complex)
            Compare_INDEL(INDEL_vcf_HC,INDEL_Gold_simple_HC,INDEL_Gold_complex_HC,file_out_dir)
        else:
            Compare_INDEL(vcf_indel,INDEL_Gold_simple,INDEL_Gold_complex,file_out_dir)
        print("INDEL evaluation finished")

    if sv_flag or all_flag:
        print("SV evaluation start")
        vcf_sv = vcfdict_SV(vcf_file)
        SV_Gold_simple,SV_Gold_complex = GetGoldSV(gold_file)
        if bed_file:
            SV_vcf_HC = SplitHiconf(bed,vcf_sv)
            SV_Gold_simple_HC = SplitHiconf(bed,SV_Gold_simple)
            SV_Gold_complex_HC = SplitHiconf(bed,SV_Gold_complex)
            Compare_SV(SV_vcf_HC,SV_Gold_simple_HC,SV_Gold_complex_HC,file_out_dir)
        else:
            Compare_SV(vcf_sv,SV_Gold_simple,SV_Gold_complex,file_out_dir)
        print("SV evaluation finished")
    
    print("All Done!")
    print("Total time:",time.time()-t)
        
            

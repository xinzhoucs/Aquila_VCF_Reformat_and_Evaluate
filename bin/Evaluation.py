from hc_common import GetBed,SplitHiconf
from indel import GetGoldINDEL,Compare_INDEL,vcfdict_INDEL
from snp import GetGoldSNP,Compare_SNP,vcfdict_SNP
from sv import GetGoldSV,Compare_SV,vcfdict_SV
from argparse import ArgumentParser
import time

parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n liuyichen@std.uestc.edu.cn\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--bed_hc','-b',help="Bed file which represents high confidence region",default="none")
parser.add_argument('--gold_gz','-g',help="Gold standard vcf file (gziped)",required=True)
parser.add_argument('--vcf_file','-v',help="Vcf file to be evaluated",required=True)
args = parser.parse_args()


if __name__ == "__main__":
    bed_file = args.bed_hc
    vcf_file = args.vcf_file
    gold_file = args.gold_gz
    t = time.time()
    if bed_file!="none":
        bed = GetBed(bed_file)
    print("SNP evaluation start")
    vcf_snp = vcfdict_SNP(vcf_file)
    gold_snp = GetGoldSNP(gold_file)
    if bed_file!="none":
        SNP_vcf_HC = SplitHiconf(bed,vcf_snp)
        Gold_SNP_HC = SplitHiconf(bed,gold_snp)
        Compare_SNP(SNP_vcf_HC,Gold_SNP_HC)
    else:
        Compare_SNP(vcf_snp,gold_snp)
    print("SNP evaluation finished")
    print("INDEL evaluation start")
    vcf_indel = vcfdict_INDEL(vcf_file)
    INDEL_Gold_simple,INDEL_Gold_complex = GetGoldINDEL(gold_file)
    if bed_file!="none":
        INDEL_vcf_HC = SplitHiconf(bed,vcf_indel)
        INDEL_Gold_simple_HC = SplitHiconf(bed,INDEL_Gold_simple)
        INDEL_Gold_complex_HC = SplitHiconf(bed,INDEL_Gold_complex)
        Compare_INDEL(INDEL_vcf_HC,INDEL_Gold_simple_HC,INDEL_Gold_complex_HC)
    else:
        Compare_INDEL(vcf_indel,INDEL_Gold_simple,INDEL_Gold_complex)
    print("INDEL evaluation finished")
    print("SV evaluation start")
    vcf_sv = vcfdict_SV(vcf_file)
    SV_Gold_simple,SV_Gold_complex = GetGoldSV(gold_file)
    if bed_file!="none":
        SV_vcf_HC = SplitHiconf(bed,vcf_sv)
        SV_Gold_simple_HC = SplitHiconf(bed,SV_Gold_simple)
        SV_Gold_complex_HC = SplitHiconf(bed,SV_Gold_complex)
        Compare_SV(SV_vcf_HC,SV_Gold_simple_HC,SV_Gold_complex_HC)
    else:
        Compare_SV(vcf_sv,SV_Gold_simple,SV_Gold_complex)
    print("SV evaluation finished")
    print("All Done!")
    print("Total time:",time.time()-t)
        
            

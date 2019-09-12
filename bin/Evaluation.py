from hc_common import GetBed,SplitHiconf
from indel import GetGoldINDEL,Compare_INDEL,vcfdict_INDEL
from snp import GetGoldSNP,Compare_SNP,vcfdict_SNP
from argparse import ArgumentParser
import time

parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n liuyichen@std.uestc.edu.cn\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--bed_hc','-b',help="Bed file which represents high confidence region",required=True)
parser.add_argument('--gold_gz','-g',help="Gold standard vcf file (gziped)",required=True)
parser.add_argument('--vcf_file','-v',help="Vcf file to be evaluated",required=True)
args = parser.parse_args()


if __name__ == "__main__":
    bed_file = args.bed_hc
    vcf_file = args.vcf_file
    gold_file = args.gold_gz
    t = time.time()
    bed = GetBed(bed_file)
    print("SNP evaluation start")
    SNP_vcf_HC = SplitHiconf(bed,vcfdict_SNP(vcf_file))
    Gold_SNP_HC = SplitHiconf(bed,GetGoldSNP(gold_file))
    Compare_SNP(SNP_vcf_HC,Gold_SNP_HC)
    print("SNP evaluation finished")
    print("INDEL evaluation start")
    INDEL_vcf_HC = SplitHiconf(bed,vcfdict_INDEL(vcf_file))
    INDEL_Gold_simple,INDEL_Gold_complex = GetGoldINDEL(gold_file)
    INDEL_Gold_simple_HC = SplitHiconf(bed,INDEL_Gold_simple)
    INDEL_Gold_complex_HC = SplitHiconf(bed,INDEL_Gold_complex)
    Compare_INDEL(INDEL_vcf_HC,INDEL_Gold_simple_HC,INDEL_Gold_complex_HC)
    print("INDEL evaluation finished")
    print("All Done!")
    print("Total time:",time.time()-t)
        
            
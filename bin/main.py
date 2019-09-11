from check_and_modify import *
from HC_common import GetBed,SplitHiconf
from indel import GetGoldINDEL,Compare_INDEL,vcfdict_INDEL
from snp import GetGoldSNP,Compare_SNP,vcfdict_SNP
import time


check_pos_flag = True
modify_flag = True
ref_genome = "E:/LEARN/Summer/source/genome.fa"
vcf_file = "E:/LEARN/Summer/source/Aquila_final_sorted.vcf"
vcfwrite = "E:/LEARN/Summer/source/Aquila_Reformated.vcf" 

SNP_flag = True
INDEL_flag = True
bed_file = "E:/LEARN/Summer/source/HG001_Gold.bed"
gold_file = "E:/LEARN/Summer/source/HG001_Gold.gz"

if __name__ == "__main__":
    t = time.time()
    if check_pos_flag or modify_flag:
        genome = GetGenoSeq(ref_genome)
        if check_pos_flag:
            print("Coordinate check start")
            check_pos(vcf_file,genome)
            print("Coordinate check finished")
        if modify_flag:
            print("Vcf reformat start")
            modify(vcf_file,genome,vcfwrite)
            print("Vcf reformat finished")
    #===================================================
    if (SNP_flag or INDEL_flag) and modify_flag:
        vcf_file = vcfwrite
    #===================================================
    if SNP_flag or INDEL_flag:
        bed = GetBed(bed_file)
        if SNP_flag:
            print("SNP evaluation start")
            SNP_vcf_HC = SplitHiconf(bed,vcfdict_SNP(vcf_file))
            Gold_SNP_HC = SplitHiconf(bed,GetGoldSNP(gold_file))
            Compare_SNP(SNP_vcf_HC,Gold_SNP_HC)
            print("SNP evaluation finished")
        if INDEL_flag:
            print("INDEL evaluation start")
            INDEL_vcf_HC = SplitHiconf(bed,vcfdict_INDEL(vcf_file))
            INDEL_Gold_simple,INDEL_Gold_complex = GetGoldINDEL(gold_file)
            INDEL_Gold_simple_HC = SplitHiconf(bed,INDEL_Gold_simple)
            INDEL_Gold_complex_HC = SplitHiconf(bed,INDEL_Gold_complex)
            Compare_INDEL(INDEL_vcf_HC,INDEL_Gold_simple_HC,INDEL_Gold_complex_HC)
            print("INDEL evaluation finished")
    print("All Done!")
    print("Total time:",time.time()-t)
        
            
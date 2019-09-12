import gzip

def GetGoldSNP(gzpath):
    dic_gold = {}
    with gzip.open(gzpath,"rb") as f:
        for line in f:
            line = line.decode('utf-8')
            if line[0] != '#':
                line = line.split('\t')
                TYPE = line[9].split(":")[0]
                TYPE = int(TYPE[0])*int(TYPE[2])
                if TYPE ==2:
                    alt1,alt2 = line[4].split(",")
                    CHROM = line[0]
                    POS = int(line[1])
                    REF = line[3]
                    ALT = line[4]
                    if len(REF)==len(alt1)==1:
                        dic_gold[(CHROM,POS,REF,alt1)] = 0
                    if len(REF)==len(alt2)==1:
                        dic_gold[(CHROM,POS,REF,alt2)] = 0
                    if REF[0]!=alt1[0] and REF[1:]==alt1[1:] and len(REF)>1:
                        dic_gold[(CHROM,POS,REF,alt1)] = 0
                    if REF[0]!=alt2[0] and REF[1:]==alt2[1:] and len(REF)>1:
                        dic_gold[(CHROM,POS,REF,alt2)] = 0
                elif len(line[3])==len(line[4])==1:
                    CHROM = line[0]
                    POS = int(line[1])
                    REF = line[3]
                    ALT = line[4]
                    dic_gold[(CHROM,POS,REF,ALT)] = TYPE

    return dic_gold

def vcfdict_SNP(vcf_file):
    dic = {}
    with open(vcf_file,'r') as vcf:
        for line in vcf:
            if line[0] != '#':
                line = line.split('\t')
                if line[7] == "SVTYPE=SNP":
                    CHROM = line[0]
                    POS = int(line[1])
                    REF = line[3]
                    ALT = line[4]
                    TYPE = line[9].split(":")[0]
                    TYPE = int(TYPE[0])*int(TYPE[2])
                    if TYPE == 2:
                        alt1,alt2 = ALT.split(",")
                        dic[(CHROM,POS,REF,alt1)] = 0
                        dic[(CHROM,POS,REF,alt2)] = 0
                    else:
                        dic[(CHROM,POS,REF,ALT)] = TYPE
    return dic

def Compare_SNP(libdic,gold):
    overlap = 0
    fn=0
    fp=0
    gtc = 0
    he_ho = 0
    ho_he = 0
    for key,item in libdic.items():
        if key in gold:
            #overlap[keyo] = itemo
            overlap+=1
            if item == gold[key]:
                gtc+=1
            elif item == 1 and gold[key] == 0:
                he_ho+=1
            elif item == 0 and gold[key] == 1:
                ho_he+=1
        else:
            fp+=1
    for keyg in gold.keys():
        if keyg not in libdic:
            fn+=1
    print("SNP:")
    print("\tOverlap",overlap,"\n\tFP",fp,"\n\tFN",fn)
    print("\tTotal gold:",len(gold),"\n\tTotal input vcf:",len(libdic))
    print("\tPrecision(overlap/input_vcf)",overlap/(overlap+fp))
    print("\tRecall(sensitivity,overlap/gold)",overlap/len(gold))
    print("----------------------------------")
    print("\tGenoType correct:",gtc)
    print("\tHetero(Gold) -> Homo (input_vcf):",he_ho)
    print("\tHomo(Gold) -> Hetero (input_vcf):",ho_he)
    print("\tTotal GenoType change:",he_ho+ho_he)
    print("\tGenoType error rate:",(he_ho+ho_he)/overlap)
    print("--------------------------------------------------------------------------\n")

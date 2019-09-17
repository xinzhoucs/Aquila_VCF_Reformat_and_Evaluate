import gzip

def GetGoldINDEL(gzpath):
    simple_gold = {}
    complex_gold = {}
    with gzip.open(gzpath,"rb") as f:
        for line in f:
            line = line.decode('utf-8')
            if line[0] != '#':
                line = line.split('\t')
                TYPE = line[9].split(":")[0]
                TYPE = int(TYPE[0])*int(TYPE[2])
                if TYPE ==2:
                    alt1,alt2 = line[4].split(",")
                    if len(line[3])!=1 or len(alt1)!=1 or len(alt2)!=1:
                        CHROM = line[0]
                        POS = int(line[1])
                        complex_gold[(CHROM,POS,line[3],line[4])]= TYPE
                elif len(line[3])!=1 or len(line[4])!=1:
                    if abs(len(line[3])-len(line[4]))<50:
                        CHROM = line[0]
                        POS = int(line[1])
                        simple_gold[(CHROM,POS,line[3],line[4])]= TYPE
    return simple_gold , complex_gold

def vcfdict_INDEL(vcf_file):
    dic = {}
    with open(vcf_file,'r') as vcf:
        for line in vcf:
            if line[0] != '#':
                line = line.split('\t')
                if line[7] != "SVTYPE=SNP":
                    if abs(len(line[3])-len(line[4]))<50:
                        #print(line)
                        CHROM = line[0]
                        POS = int(line[1])
                        TYPE = line[9].split(":")[0]
                        TYPE = int(TYPE[0])*int(TYPE[2])
                        dic[(CHROM,POS,line[3],line[4])]= TYPE
    return dic

def very_complex(ref,alt1,alt2):
    if ref[0]!=alt1[0] or ref[0]!=alt2[0]:
        return True
    else:
        return False

def split_value(ref,alt):
    R = len(ref)
    A = len(alt)
    if R>A:
        if A>1:
            refnew = ref[:-(A-1)]
            altnew = alt[0]
        else:
            refnew = ref
            altnew = alt
    elif R<A:
        if R>1:
            refnew = ref[0]
            altnew = alt[:-(R-1)]
        else:
            refnew = ref
            altnew = alt
    else:
        print(ref,alt)
        refnew = "N/A"
        altnew = "N/A"
    return refnew,altnew

def split_complex(complex_dic):
    split_dic = {}
    for key in complex_dic.keys():
        ref = key[2]
        alt1,alt2 = key[3].split(",")
        pos = key[1]
        if not very_complex(ref,alt1,alt2):
            ref1,alt1 = split_value(ref,alt1)
            if abs(len(ref1)-len(alt1)) <50:
                split_dic[(key[0],pos,ref1,alt1)] = 0
            ref2,alt2 = split_value(ref,alt2)
            if abs(len(ref2)-len(alt2)) <50:
                split_dic[(key[0],pos,ref2,alt2)] = 0
    return split_dic

def Compare_INDEL(libdic,gold,gold_complex):
    #overlap = {}
    overlap = 0
    fn=0
    fp=0
    gtc = 0
    he_ho = 0
    ho_he = 0
    split_comp = split_complex(gold_complex)
    
    for key,item in libdic.items():
        if key in gold:
            #overlap[keyo] = itemo
            overlap+=1
            if item == gold[key]:
                gtc+=1
            elif item == 1 and gold[key] != 1:
                he_ho+=1
            elif item != 1 and gold[key] == 1:
                ho_he+=1
            else:
                print(item,gold[key])
        elif key in split_comp:
            overlap+=1
            if item == split_comp[key]:
                gtc+=1
            elif item == 1 and split_comp[key] != 1:
                he_ho+=1
            else:
                print(item,gold[key])
        else:
            fp+=1
    for key in gold.keys():
        if key not in libdic:
            fn+=1
    for key in split_comp.keys():
        if key not in libdic:
            fn+=1
#=======================================================
    #total = len(split_comp)
    pos_time = {}
    time_data = {}
    comp_lap = 0
    for key in split_comp.keys():
        #total+=1
        if key in libdic:
            comp_lap += 1
            if (key[0],key[1]) in pos_time:
                pos_time[(key[0],key[1])] +=1
            else:
                pos_time[(key[0],key[1])] = 1
        else:
            if (key[0],key[1]) not in pos_time:
                pos_time[(key[0],key[1])] = 0
    for value in pos_time.values():
        if value in time_data:
            time_data[value] += 1
        else:
            time_data[value] = 1
    print("INDEL:")
    print("\tOverlap",overlap,"\n\tFP",fp,"\n\tFN",fn)
    print("\tTotal gold:",len(gold)+len(split_comp),"\n\tTotal input vcf:",len(libdic))
    print("\tPrecision(overlap/input_vcf)",overlap/(overlap+fp))
    print("\tRecall(sensitivity,overlap/gold):",overlap/(len(gold)+len(split_comp)))
    print("----------------------------------")
    print("\tGenoType correct:",gtc)
    print("\tHetero(Gold) -> Homo (input_vcf):",he_ho)
    print("\tHomo(Gold) -> Hetero (input_vcf):",ho_he)
    print("\tTotal GenoType change:",he_ho+ho_he)
    print("\tGenoType error rate:",(he_ho+ho_he)/overlap)
    print("----------------------------------")
    print("\tCompound:")
    for key,value in time_data.items():
        print("\tfind",key,"times:",value)
        
    #print("Total:",total,"Overlap:",comp_lap)
    print("--------------------------------------------------------------------------\n")

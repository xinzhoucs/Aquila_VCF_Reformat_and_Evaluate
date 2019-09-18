def takeFirst(elem):
    return elem[0]
    
def TRgt100(region_list,start,end,lenth):
    overlap = 0
    for pair in region_list:
        if start<=pair[0]<=end and start<=pair[1]<=end:
            overlap = overlap+pair[1]-pair[0]+1
        elif pair[0]<start and start<=pair[1]<=end:
            overlap = overlap+pair[1]-start+1
        elif pair[0]<=start and pair[1]>=end:
            overlap = lenth
            break
        elif start<=pair[0]<=end and pair[1]>=end:
            overlap = overlap+end-pair[0]+1
            break
        elif end<pair[0]:
            break
    rate = overlap/lenth
    if rate>=0.2:
        return True
    else:
        return False

def noTRgt100(vcf,TRmask,noTR100vcf):
    mask = {}
    notTR = 0
    with open(TRmask,"r") as ftr:
        for line in ftr:
            line = line.split("\t")
            if line[0] not in mask:
                mask[line[0]] = [(int(line[1]),int(line[2]))]
            else:
                mask[line[0]].append((int(line[1]),int(line[2])))
    for key in mask.keys():
        mask[key].sort(key=takeFirst)

    with open(noTR100vcf,"w") as fw:
        with open(vcf,"r") as fv:
            for line in fv:
                if line[0] == "#":
                    fw.write(line)
                else:
                    line = line.split("\t")
                    CHROM = line[0]
                    start = int(line[1])
                    end = start+len(line[3])-1
                    lenth = end-start+1
                    if not TRgt100(mask[CHROM],start,end,lenth):
                        fw.write("\t".join(line))
                        notTR+=1
    print(notTR)

if __name__ == "__main__":
    with open("/oak/stanford/groups/arend/Xin/AssemblyProj/reference_align_2/Repeats_mask/allrepeats_byxin.bed","r") as fr:
        with open("/oak/stanford/groups/arend/Xin/LiuYC/Truvari_test/TRmask.bed","w") as fw:
            for line in fr:
                if line[0]!="#":
                    line = line.split("\t")
                    CHROM = line[5]
                    start = int(line[6])
                    end = int(line[7])
                    lenth = end-start+1
                    if lenth >= 100:
                        fw.write("%s\t%s\t%s\n"%(CHROM,start,end))

    noTRgt100("/oak/stanford/groups/arend/Xin/LiuYC/Truvari_test/outputL5+L6_hg19_v0.6_Tier1bed/fp.vcf",
            "/oak/stanford/groups/arend/Xin/LiuYC/Truvari_test/TRmask.bed",
            "/oak/stanford/groups/arend/Xin/LiuYC/Truvari_test/outputL5+L6_hg19_v0.6_Tier1bed/fp_noTRgt100.vcf")



def GetBed(bedpath):
    with open (bedpath,"r") as bed:
        bed_dic = {}
        CHROM = ''
        for line in bed:
            line = line.split('\t')
            if line[0]==CHROM:
                bed_dic[CHROM].append([int(line[1]),int(line[2])])
            else:
                bed_dic[line[0]]=[[int(line[1]),int(line[2])]]
                CHROM = line[0]
    return bed_dic

def find_pos(blocks,pos,start,end):
    mid = (start+end)//2
    if pos > blocks[end][1]:
        return False
    if pos > blocks[mid][1]:
        if pos < blocks[mid+1][0]:
            return False
        elif pos <= blocks[mid+1][1]:
            return True
        else:
            start = mid
            return find_pos(blocks,pos,start,end)
    elif pos < blocks[mid][0]:
        if mid == 0:
            return False
        else:
            end = mid
            return find_pos(blocks,pos,start,end)
    else:
        #prnt(start,end)
        return True
    
def SplitHiconf(bed_dic,dic_origin):
    dic_in = {}
    for key,item in dic_origin.items():
        if key[0] in bed_dic:
            if find_pos(bed_dic[key[0]],key[1],0,len(bed_dic[key[0]])-1):
                dic_in[key]=item
    return dic_in
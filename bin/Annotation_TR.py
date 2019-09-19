import tarfile
import os
from argparse import ArgumentParser

parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n liuyichen@std.uestc.edu.cn\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input','-i',help="Input fp,fn of tp result txt",required = True)
parser.add_argument('--output','-o',help="Output file",required=True)
args = parser.parse_args()

def takeFirst(elem):
    return elem[0]
    
def find_pos(blocks,pos,start,end):
    mid = (start+end)//2
    if pos > blocks[end][1]:
        return (end,end+1,"out")
    elif pos < blocks[start][0]:
        return (start-1,start,"out")
    elif pos > blocks[mid][1]:
        if pos < blocks[mid+1][0]:
            return (mid,mid+1,"out")
        elif pos <= blocks[mid+1][1]:
            return (mid+1,mid+1,"in")
        else:
            start = mid
            return find_pos(blocks,pos,start,end)
    elif pos < blocks[mid][0]:
        end = mid
        return find_pos(blocks,pos,start,end)
    else:
        return (mid,mid,"in")

def TRgt100(txt,TRmask,TR100txt):
    mask = {}
    with open(TRmask,"r") as ftr:
        for line in ftr:
            line = line.split("\t")
            if line[0] not in mask:
                mask[line[0]] = [(int(line[1]),int(line[2]))]
            else:
                mask[line[0]].append((int(line[1]),int(line[2])))
    for key in mask.keys():
        mask[key].sort(key=takeFirst)

    with open(TR100txt,"w") as fw:
        with open(txt,"r") as fv:
            for line in fv:
                overlap = 0
                line_split = line.split("\t")
                CHROM = line_split[0]
                start = int(line_split[1])
                end = start+len(line_split[2])-1
                blocks = mask[CHROM]
                lenth = end-start+1

                start_block = find_pos(blocks,start,0,len(blocks)-1)
                end_block = find_pos(blocks,end,0,len(blocks)-1)

                #if start_block[1] == len(blocks):
                    #fw.write(line.replace("\n","\tnoTRgt100\n"))

                #elif end_block[0] == -1:
                    #fw.write(line.replace("\n","\tnoTRgt100\n"))

                if start_block[2] == "in" and end_block[2] == "in":
                    if start_block[0] == end_block[0]:
                        fw.write(line.replace("\n","\tTRgt100\n"))
                    else:
                        overlap = overlap+blocks[start_block[0]][1]-start+end-blocks[end_block[0]][0]+2
                        for i in range(start_block[0]+1,end_block[0]):
                            overlap = overlap+blocks[i][1]-blocks[i][0]+1
                        if overlap/lenth >= 0.2:
                            fw.write(line.replace("\n","\tTRgt100\n"))
                        else:
                            fw.write(line.replace("\n","\tnoTRgt100\n"))

                elif start_block[2] == "out" and end_block[2] == "in":
                    overlap = overlap+end-blocks[end_block[0]][0]+1
                    for i in range(start_block[1],end_block[0]):
                        overlap = overlap+blocks[i][1]-blocks[i][0]+1
                    if overlap/lenth >= 0.2:
                        fw.write(line.replace("\n","\tTRgt100\n"))
                    else:
                        fw.write(line.replace("\n","\tnoTRgt100\n"))

                elif start_block[2] == "in" and end_block[2] == "out":
                    overlap = overlap+blocks[start_block[0]][1]-start+1
                    for i in range(start_block[0]+1,end_block[1]):
                        overlap = overlap+blocks[i][1]-blocks[i][0]+1
                    if overlap/lenth >= 0.2:
                        fw.write(line.replace("\n","\tTRgt100\n"))
                    else:
                        fw.write(line.replace("\n","\tnoTRgt100\n"))

                elif start_block[2] == "out" and end_block[2] == "out":
                    if start_block[0] == end_block[0]:
                        fw.write(line.replace("\n","\tnoTRgt100\n"))
                    else:
                        for i in range(start_block[1],end_block[1]):
                            overlap = overlap+blocks[i][1]-blocks[i][0]+1
                        if overlap/lenth >= 0.2:
                            fw.write(line.replace("\n","\tTRgt100\n"))
                        else:
                            fw.write(line.replace("\n","\tnoTRgt100\n"))

if __name__ == "__main__":
    txt = args.input
    TR100txt = args.output
    script_path = os.path.dirname(os.path.abspath( __file__ ))
    code_path = script_path + "/" 
    if not os.path.exists(code_path+"TRmask.bed"):
        trmask = tarfile.open(code_path+"TRmask.bed.tar.gz","r")
        for ti in trmask:
            trmask.extract(ti,code_path)
        trmask.close()
    TRgt100(txt,code_path+"TRmask.bed",TR100txt)

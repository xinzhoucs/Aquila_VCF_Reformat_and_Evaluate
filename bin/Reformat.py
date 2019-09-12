from argparse import ArgumentParser
import time

parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n liuyichen@std.uestc.edu.cn\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--ref_fa','-r',help="Reference fasta file for reformat",required=True)
parser.add_argument('--in_vcf','-i',help="Original vcf file",required=True)
parser.add_argument('--out_vcf','-o',help="Output reformated vcf file",required=True)
args = parser.parse_args()


def GetGenoSeq (fafile):
    genome ={}
    chro = []
    chrnum = ""
    with open(fafile,"r") as f:
        for line in f:
            if line.startswith('>'):
                if chro:
                    genome[chrnum] = ''.join(chro)
                    chro = []
                chrnum = line[1:].split(' ')[0].strip('\n')
            else:
                chro.append(line.strip('\n'))
        genome[chrnum] = ''.join(chro)
        chro = []
    return genome
    
def modify(vcf_file,genome,vcfwrite):
    chrom_list = ['chr1','chr2','chr3','chr4','chr5',
                  'chr6','chr7','chr8','chr9','chr10',
                  'chr11','chr12','chr13','chr14','chr15',
                  'chr16','chr17','chr18','chr19','chr20',
                  'chr21','chr22','chrX']
    with open (vcf_file, "r") as f:
        with open (vcfwrite,"w") as fw:
            for line in f:
                if line[0] == '#':
                    fw.write(line)
                else:
                    line = line.split('\t')
                    POS = int(line[1])
                    CHROM = line[0]
                    INFO = line[7]
                    line[3] = line[3].upper()
                    line[4] = line[4].upper()
                    if CHROM in chrom_list:
                        if INFO == 'SVTYPE=SNP':
                            line[1] = str(POS+1)
                            fw.write('\t'.join(line))
                        elif INFO == 'SVTYPE=DEL':
                            line[3] = genome[CHROM][POS-1].upper() + line[3]
                            line[4] = genome[CHROM][POS-1].upper()
                            line[1] = str(POS)
                            fw.write('\t'.join(line))
                        else:#INFO == 'VTYPE=INS'
                            line[3] = genome[CHROM][POS-1].upper()
                            line[4] = genome[CHROM][POS-1].upper() + line[4]
                            line[1] = str(POS)
                            fw.write('\t'.join(line))

if __name__ == "__main__":
    ref_genome = args.ref_fa
    vcf_file = args.in_vcf
    vcfwrite = args.out_vcf
    print("Vcf reformat start")
    t = time.time()
    genome = GetGenoSeq(ref_genome)
    modify(vcf_file,genome,vcfwrite)
    print("Vcf reformat finished")
    print("Time used:",time.time()-t)
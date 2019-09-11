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


def check_pos(vcf_file,genome,svtype="SNP"):
    count0= 0
    count1= 0
    count = 0
    countelse = 0
    chrom_list = ['chr1','chr2','chr3','chr4','chr5',
                  'chr6','chr7','chr8','chr9','chr10',
                  'chr11','chr12','chr13','chr14','chr15',
                  'chr16','chr17','chr18','chr19','chr20',
                  'chr21','chr22','chrX']
    with open (vcf_file, "r") as f:
        for line in f:
            if line[0] != '#':
                line = line.split('\t')
                POS0 = int(line[1])#coordinate start from 0
                POS1 = POS0-1      #coordinate start from 1
                CHROM = line[0]
                INFO = line[7]
                if INFO == 'SVTYPE='+svtype and CHROM in chrom_list:
                    count += 1
                    if genome[CHROM][POS0:POS0+len(line[3])].upper() == line[3].upper():
                        count0 += 1
                    elif genome[CHROM][POS1:POS1+len(line[3])].upper() == line[3].upper():
                        count1 += 1
                    else:
                        countelse +=1
                        print("EXCEPTION:")
                        print('VCF',line[3].upper())
                        print('GENOME',genome[CHROM][POS0:POS0+len(line[3])].upper(),POS0,len(genome[CHROM]),CHROM)
    print("Total SNP:",count)
    print("start from 0:",count0)
    print("start from 1:",count1)
    print("Neither 0 nor 1 (exceptions):",countelse)
    print("--------------------------------------------------------------------------\n")
    
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
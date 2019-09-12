# Vcf Reformat and Evaluate
## Reformat:
### Example:
```
python Reformat.py -r ../source/genome.fa -i ../source/Aquila_final_sorted.vcf -o ../source/Aquila_Reformated.vcf 
```
### *Required parameters
#### --ref_fa REF_FA, -r REF_FA : Reference fasta file for reformat
#### --in_vcf IN_VCF, -i IN_VCF : Original vcf file
#### --out_vcf OUT_VCF, -o OUT_VCF : Output reformated vcf file

## Evaluate:
### Example:
```
python Evaluation.py -b ../source/HG001_Gold.bed -g ../source/HG001_Gold.gz -v ../source/L2_stLFR_L3_10x.vcf
```
### *Required parameters
#### --bed_hc BED_HC, -b BED_HC : Bed file which represents high confidence region
#### --gold_gz GOLD_GZ, -g GOLD_GZ : Gold standard vcf file (gziped)
#### --vcf_file VCF_FILE, -v VCF_FILE : Vcf file to be evaluated


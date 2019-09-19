# Vcf Reformat and Evaluate
## Reformat: Reformat VCF files from Aquila to do variants calling evaluation (by Evaluation.py or RTGtools/hap.py) 
Reformat script modify the REF field, ALT field and POS field as follows:
```
All Variants Changes from base 0 to base 1 (optional with flag "--base_norm")

For INDEL/SV:
acg     -    =>     TACG        T
                      ^         ^
               lower to upper   add one reference base (optional with flag "--base_norm")
               (default)   

For SNP:
a     t    =>     A        T
                  ^        ^
               lower to upper 
               (default)
```
### Example:
```
python Reformat.py -r ./source/genome.fa -i /PATH/TO/Aquila_final_sorted.vcf -o Aquila_Reformated.vcf 
```
### *Required parameters
#### --ref_fa REF_FA, -r REF_FA : Reference fasta file for reformat
#### --in_vcf IN_VCF, -i IN_VCF : Original vcf file from Aquila
#### --out_vcf OUT_VCF, -o OUT_VCF : Output reformated vcf file
### *Optional parameters
#### --add_header HEADER, -head HEADER : Add header to vcf (38,19 or none), default=False
#### --add_chr,-ac : If set, the script will add 'chr' to CHROM field (1->chr1), default=False
#### --gz_tbi,-gt : If set, the script will output gz and tbi file (requires htslib,tabix and vcftools package), default=False
#### --base_norm,-bn : If set, change base from 0 to 1 (for all types of variants) and add 1 base at the beginning for both REF and ALT fields of INDEL/SV (see above schematic diagram). default=False 

## Evaluate:
### Example:
```
python Evaluation.py -b ../source/HG001_Gold.bed -g ../source/HG001_Gold.gz -v ../source/L2_stLFR_L3_10x.vcf
```
### *Required parameters
#### --gold_gz GOLD_GZ, -g GOLD_GZ : Gold standard vcf file (gziped)
#### --vcf_file VCF_FILE, -v VCF_FILE : Vcf file to be evaluated
### *Optional parameters
#### --bed_hc BED_HC, -b BED_HC : Bed file which represents region you want to evaluate. default = False
#### --file_out_dir DIR, -o DIR : If set, evaluate resilts (snp_tp.txt, snp_fp.txt, snp_fn.txt, and etc) will be outputed to the specified dir. default = False
#### --snp_eval,-snp : If set, evaluate SNP in input vcf file (if none of snp,sv,indel flag is set, ALL of them will be evaluated)
#### --sv_eval,-sv : If set, evaluate SV in input vcf file (if none of snp,sv,indel flag is set, ALL of them will be evaluated)
#### --indel_eval,-indel : If set, evaluate INDEL in input vcf file (if none of snp,sv,indel flag is set, ALL of them will be evaluated)
### Output Example
```
SNP evaluation start
SNP:
        Overlap 3012536
        FP 102492
        FN 32558
        Total gold: 3045094
        Total input vcf: 3115028
        Precision(overlap/input_vcf) 0.9670975670202644
        Recall(sensitivity,overlap/gold) 0.9893080476333407
----------------------------------
        GenoType correct: 3007594
        Hetero(Gold) -> Homo (input_vcf): 3865
        Homo(Gold) -> Hetero (input_vcf): 1077
        Total GenoType change: 4942
        GenoType error rate: 0.001640478321254916
--------------------------------------------------------------------------

SNP evaluation finished
INDEL evaluation start
INDEL:
        Overlap 500104
        FP 28148
        FN 31278
        Total gold: 531382
        Total input vcf: 528252
        Precision(overlap/input_vcf) 0.9467148254999508
        Recall(sensitivity,overlap/gold): 0.9411383900847224
----------------------------------
        GenoType correct: 490361
        Hetero(Gold) -> Homo (input_vcf): 3256
        Homo(Gold) -> Hetero (input_vcf): 6487
        Total GenoType change: 9743
        GenoType error rate: 0.019481947754866988
----------------------------------
        Compound:
        find 1 times: 11841
        find 0 times: 694
        find 2 times: 20397
--------------------------------------------------------------------------

INDEL evaluation finished
SV evaluation start
SV:
        Overlap 9
        FP 2716
        FN 0
        Total gold: 9
        Total input vcf: 2725
        Precision(overlap/input_vcf) 0.0033027522935779817
        Recall(sensitivity,overlap/gold): 1.0
----------------------------------
        GenoType correct: 8
        Hetero(Gold) -> Homo (input_vcf): 0
        Homo(Gold) -> Hetero (input_vcf): 1
        Total GenoType change: 1
        GenoType error rate: 0.1111111111111111
----------------------------------
        Compound:
--------------------------------------------------------------------------

SV evaluation finished
All Done!
Total time: 108.1656060218811
```

## TRgt100 Annotation
### Example
```
python Annotation_TR.py -i INDEL_fp.txt -o INDEL_fp_TR.txt
```
### *Required parameters
#### --input FILE, -i FILE : Input file is the output by "Evaluation.py". 
#### --output FILE, -o FILE : Output file with one more field (TRgt100 Annotation). 

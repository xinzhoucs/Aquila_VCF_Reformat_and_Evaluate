# Vcf Reformat and Evaluate
## Reformat:
Reformat script modify the REF field, ALT field and POS field as follows:
```
For INDEL:
acg     -    =>     TACG        T
                      ^         ^
               lower to upper   add one reference base

For SNP:
lower to upper and POS add 1 (Coordinate change from 0 to 1)
```
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
All Done!
Total time: 82.49052119255066
```

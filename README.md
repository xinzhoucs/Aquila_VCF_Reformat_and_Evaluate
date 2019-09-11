# Check_Reformat_Evaluate
## Input Example:
```
check_pos_flag = True
modify_flag = True
ref_genome = "E:/LEARN/Summer/source/genome.fa"
vcf_file = "E:/LEARN/Summer/source/Aquila_final_sorted.vcf"
vcfwrite = "E:/LEARN/Summer/source/Aquila_Reformated.vcf" 

SNP_flag = True
INDEL_flag = True
bed_file = "E:/LEARN/Summer/source/HG001_Gold.bed"
gold_file = "E:/LEARN/Summer/source/HG001_Gold.gz"
```

## Output Example
```
Coordinate check start
Total SNP: 3971444
start from 0: 3971444
start from 1: 0
Neither 0 nor 1 (exceptions): 0
--------------------------------------------------------------------------

Coordinate check finished
Vcf reformat start
Vcf reformat finished
SNP evaluation start
SNP:
        Overlap 3010775 
        FP 123256 
        FN 34319
        Total gold: 3045094 
        Total Aquila: 3134031
        Precision(overlap/aquila) 0.960671735538034
        Recall(sensitivity,overlap/gold) 0.9887297403626949
----------------------------------
        GT_correct: 3006103
        Hetero(Gold) -> Homo (Aquila): 3453
        Homo(Gold) -> Hetero (Aquila): 1219
        Total GT change: 4672
        Error: 0.0015517599289219554
--------------------------------------------------------------------------

SNP evaluation finished
INDEL evaluation start
INDEL:
        Overlap 499301 
        FP 40292 
        FN 32081
        Total gold: 531382
        Total Aquila: 539593
        Precision(overlap/Aquila) 0.9253289053045536
        Recall(sensitivity,overlap/gold): 0.9396272361502648
----------------------------------
        GT_correct: 489808
        Hetero(Gold) -> Homo (Aquila): 1522
        Homo(Gold) -> Hetero (Aquila): 7971
        Total GT change: 9493
        Error: 0.019012579586261593
----------------------------------
        Complex:
        find 1 times: 11894
        find 2 times: 20253
        find 0 times: 785
--------------------------------------------------------------------------

INDEL evaluation finished
All Done!
Total time: 
```

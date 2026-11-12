Step 4 of 50: training loss 1.2634, accuracy 0.6038.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   773     2   160     0     0    10    35     0    11     0
               1     0  1018    14     4     2    14     5     6     1     0
               2     6     1   625    20     3    41    39     0   255     0
               3     1     2    93   372     0   284     5     2   264     7
               4     1    35    32     2   648     3   136     1    27    98
               5     8     9    22    30     0   598   163     2    82     1
               6    48    19     8     1    42    76   723     0    50     0
               7     6     2   339    20     2    35     0   179    23   484
               8    15    41   212    16     3    41    55     3   581    42
               9    63    21    99     4    34    46    31    14   128   521

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2326 | 0.5909
2 | 1.1902 | 0.6278
3 | 2.8557 | 0.3611
4 | 1.2634 | 0.6038

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.


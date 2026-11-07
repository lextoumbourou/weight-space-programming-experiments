Step 5 of 15: validation loss 1.2362, accuracy 0.5778.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   685     8    11     1     0     0    83     4    50   149
               1     0   960    88     3     0     4     3     5     0     1
               2     8    17   518    64    15    10    34     5   151   168
               3     1    17    13   618     0   178   108    22    54    19
               4     0    46    12     0   438    10     0    44    70   363
               5     5    33    10   118     2   377   116    91    55   108
               6    16    72     8    11    29    40   501     0    39   251
               7     2    32    11    10     3    10     2   750     3   267
               8     0    80   233   119     0    30    13   103   335    96
               9     3    51     2     3    66    44     1   179    16   596

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.1586 | 0.4753
2 | 1.4530 | 0.4972
3 | 1.2907 | 0.5670
4 | 1.3876 | 0.4982
5 | 1.2362 | 0.5778

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.

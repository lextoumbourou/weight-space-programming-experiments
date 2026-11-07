Step 7 of 50: validation loss 1.1074, accuracy 0.6684.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   850    11    73     1     2     0    31     1    22     0
               1     0  1002    17     3     0     0     3    39     0     0
               2    14    22   447   179    43     4    49    12   219     1
               3     2    14     3   755     8    26    31    18   140    33
               4    10    85     1     5   680     0    58     3    17   124
               5    19    24     1   170    13   434   162    25    38    29
               6    93    73     4     7     9    10   707     0    63     1
               7    30    28    22    55    74    39     3   699    13   127
               8    10    93     3   127     7     1    99    99   473    97
               9    44    72     3    26    55     4    10    54    56   637

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273
2 | 1.4873 | 0.5904
3 | 1.5014 | 0.6332
4 | 1.5245 | 0.5778
5 | 1.1075 | 0.6597
6 | 1.1029 | 0.6659
7 | 1.1074 | 0.6684

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.

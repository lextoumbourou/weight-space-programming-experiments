Step 10 of 50: validation loss 1.1170, accuracy 0.6597.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   825     2    42     0     1     6    29     0    85     1
               1     0   953    45     2     5     1    15    43     0     0
               2     1     7   432   170    20     4    38     4   314     0
               3     0     5     2   791     3    44    14     6   156     9
               4     2    29     0     3   694     0    93     0    85    77
               5     9     7     0   124     3   533   180    12    41     6
               6    70    20     1     0     7    19   729     0   121     0
               7     6    11    32   144    68    68     2   459    43   257
               8     3    39    15    90    10     2   117    22   663    48
               9    23    31     3    34   111    11    25    15   190   518

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
8 | 2.0083 | 0.4891
9 | 1.2996 | 0.6636
10 | 1.1170 | 0.6597

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

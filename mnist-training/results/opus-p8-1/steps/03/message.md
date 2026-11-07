Step 2 of 50: validation loss 1.2930, accuracy 0.6248.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   834    15   130     0     0     3     4     5     0     0
               1     0   941    79     0     0     3     1    40     0     0
               2    33    34   671   123     5    14    39    20    51     0
               3    18    34    50   677     1   110    25    60    32    23
               4    13   147    88    11   522     1    49     7    36   109
               5    37    37    48   115     0   352   254     5    26    41
               6    67   116    27     6     2    36   706     1     6     0
               7    27    31   103    11     8    95     0   756     2    57
               8    19   139   338    26     1     2    32   115   252    85
               9    77    97   115     4    33    11    13    67     7   537

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

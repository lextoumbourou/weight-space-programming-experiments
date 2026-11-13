Step 3 of 50: training loss 0.9390, accuracy 0.7680.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   787     0   108     2     0    75    11     0     4     4
               1     3  1026    20     0     3     3     0     9     0     0
               2    27     7   657   126     6    21     4    12   126     4
               3     1     0    15   720     1   212     5     5    62     9
               4    14    19    31     6   808     5    12    10    19    59
               5    10     7    16    35     3   777    52     7     8     0
               6    51    19    39     2   234    28   585     0     7     2
               7    14     2    40    40     2    15     1   934     4    38
               8    25    20   109    13     5    15    41    35   673    73
               9    32     9     5     9     3    63    10   110     7   713

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0324 | 0.7147
2 | 0.9703 | 0.7579
3 | 0.9390 | 0.7680

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.


Step 9 of 15: validation loss 0.8746, accuracy 0.7264.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   833    13    94     0     0    11    39     0     0     1
               1     1   918    97     0     6     0     0     2    40     0
               2    71    65   663    74    37     0     4    32    31    13
               3     9     3    78   756     1   113     1    47    19     3
               4     8    26    76     5   787     0     4     2    19    56
               5     9     4    65    47     2   669    77     1    39     2
               6    30    27    30     0    67    45   713     0    11    44
               7    41    45    37    68    19    19    14   809     3    35
               8    27    76   153    13     8    17    31    37   612    35
               9    27    38    70    44    55    28    60   123    12   504

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909
5 | 0.9762 | 0.6769
6 | 0.8629 | 0.7278
7 | 0.8344 | 0.7409
8 | 0.9137 | 0.7124
9 | 0.8746 | 0.7264

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.

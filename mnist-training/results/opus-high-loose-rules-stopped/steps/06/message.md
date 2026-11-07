Step 5 of 50: validation loss 0.9636, accuracy 0.7647.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   819     0     4     1     1     0   152     0     1    13
               1     1   789   107     1     5     1    85    20    49     6
               2    12     1   638   184    20     4    47    30    42    12
               3     3     0    13   701     1   201    64     9    28    10
               4     1     8     0     1   748     1    38     1    22   163
               5     5     1     0    15     1   657   117     7   105     7
               6     2     1     0     0    11     5   923     0     5    20
               7     2     0    19     1    10     0    32   835     2   189
               8    13     4    19    26     2    13    94    15   728    95
               9     3     0     2     9     3     6    46    44    39   809

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297
5 | 0.9636 | 0.7647

45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.

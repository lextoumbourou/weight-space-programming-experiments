Step 3 of 50: validation loss 1.0920, accuracy 0.6503.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   706     5    41     6     0     7   211     0     0    15
               1     0   972    68     0     6     3     4    11     0     0
               2    15    50   579   144    41     1    32    13    25    90
               3     5    11    45   765     0    82    20    18     9    75
               4     5   121    30     1   545     1    53    35    15   177
               5     6     9    22    71     0   639   111    12    23    22
               6    96    53     4     0    23    17   745     0    10    19
               7     4    25    24     6     5     1     4   773     1   247
               8    35   190   286    43     4    24   168    82    51   126
               9    28    51    16     4     3     2    31    98     0   728

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503

47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

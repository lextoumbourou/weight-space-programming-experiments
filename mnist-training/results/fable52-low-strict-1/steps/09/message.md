Step 8 of 15: validation loss 0.9143, accuracy 0.7293.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   774     8    43     0     0     0   162     1     2     1
               1     0   818   145     0     4     6     1    89     0     1
               2    42    19   612   116    12     2     7    24   113    43
               3     3     0     9   792     1   137     4     8    71     5
               4    11    41    27     1   580     1    13    13   138   158
               5     4     7     5    45     2   702   107     8    31     4
               6    67    40     3     1    12    11   815     1    14     3
               7    33     6    15     9    15    28     8   831    10   135
               8     8    35   122    25     2     8    31    77   624    77
               9    29    13     9    11     3    14    19    86    32   745

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006
4 | 1.8724 | 0.4922
5 | 1.0033 | 0.6914
6 | 1.0466 | 0.6887
7 | 1.2388 | 0.6587
8 | 0.9143 | 0.7293

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.

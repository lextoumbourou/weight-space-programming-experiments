Step 10 of 15: validation loss 1.0173, accuracy 0.7092.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   800     7   134     0     0    16     2     0    31     1
               1     0   883    51     5    42    16     2    63     0     2
               2    29     7   620   206    68    21    12     7    19     1
               3     8     0    15   805     0   129     6     1    66     0
               4     2    16    25     7   598     5     6    15    90   219
               5     7     0     6    69     0   719    69     7    38     0
               6    42     2     9     0    25    63   816     0     9     1
               7     5     3    42    78    11     8     0   761     1   181
               8    20    17    76    88     6    94   108    58   494    48
               9    19     5    15    24     6    62     5    43   186   596

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977
4 | 1.2769 | 0.5620
5 | 1.3371 | 0.6101
6 | 1.3076 | 0.6173
7 | 2.1437 | 0.5085
8 | 1.2513 | 0.6359
9 | 1.0575 | 0.7023
10 | 1.0173 | 0.7092

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

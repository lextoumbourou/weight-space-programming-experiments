Step 8 of 15: validation loss 1.2513, accuracy 0.6359.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   784     7   156     0     0    20     2     0    22     0
               1     0   927    55     4    29    24     9    15     0     1
               2    25     8   580   231    40    43    29     3    26     5
               3     5     0    11   733     0   178     5     1    95     2
               4     2    25    25     8   590     7    32     3   131   160
               5     4     0     4    44     0   712   122     3    26     0
               6    55     3    10     6    27   201   647     0    17     1
               7     5     7   103    79    18    10     2   637     3   226
               8    12    14    81    67     4    96   244    15   394    82
               9    19     5    46    26     9    69    16    12   404   355

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

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.

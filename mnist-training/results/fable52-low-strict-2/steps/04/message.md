Step 3 of 15: validation loss 1.1485, accuracy 0.6657.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   678    19   114     0     1     6   106     1     2    64
               1     0   989    51     0     7     0     0     4     8     5
               2    39    89   449   168    47     2     1    86    31    78
               3     7     3    20   770     1    98     3    77    43     8
               4     3    15    47     1   726     0     0    15    34   142
               5     1    21    64    65     0   582    69    29    80     4
               6    16    68    59     0    99    16   585     0    72    52
               7     5     8     7    31     7    12     1   786     3   230
               8    10   207   170    23     8    15     9    91   396    80
               9    13    14    16     9    11    14    10   155    23   696

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

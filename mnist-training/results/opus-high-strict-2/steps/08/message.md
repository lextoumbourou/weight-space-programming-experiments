Step 7 of 15: validation loss 1.0119, accuracy 0.6788.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   843    17    41     0     0     7    21     1    60     1
               1     0   975    32     0     0     1     0    50     4     2
               2    13    50   652    99    32     7     4    22   110     1
               3     2     5    31   579     0   236     8    30   129    10
               4    10   101     5     5   674     0     2     4    92    90
               5    19    12     0    22    11   561   154     5   105    26
               6    81    83    17     0    76    21   657     0    29     3
               7    42    19    45    78    26     3     1   790     5    81
               8    14    81   104    35     4    13    34    41   480   203
               9    98    45    33    37    58     3    48    26    36   577

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522
5 | 1.0340 | 0.6710
6 | 1.0275 | 0.6668
7 | 1.0119 | 0.6788

8 steps left. Reply with the complete build_weights() for step 8 in one Python code block.

Step 9 of 15: validation loss 1.1631, accuracy 0.6279.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   936     5     5     0     0     0     4     0    41     0
               1     0   950    21     0     2     3     0    72    13     3
               2    93    27   502    47    58     8    14    15   219     7
               3    39     2    19   415     0   175    24    14   297    45
               4    32    38     1     1   791     0     1     0    57    62
               5    47     6     0     6    10   399   130     5   287    25
               6   139    60     0     0   112     0   564     0    90     2
               7   124     7    47    76    38     3     1   596    20   178
               8    66    47    19     2     7     2    31    20   556   259
               9   202    27     5     8    46     2     5    12    84   570

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
8 | 1.0305 | 0.6521
9 | 1.1631 | 0.6279

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.

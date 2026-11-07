Step 8 of 15: validation loss 1.0305, accuracy 0.6521.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   795    19    30     1     0    15     4     0   127     0
               1     0   946    37     0     1     3     1    73     3     0
               2    12    44   597   113    26     6    10    34   148     0
               3     3     3    21   390     0   321     0    15   250    27
               4     7    44     8     5   716     1     1     1   144    56
               5    11    13     4     7     6   627    68     3   169     7
               6    26    31     9     1    82     2   723     0    93     0
               7    27    56    47    98    12     4     0   627    22   197
               8    10    78   157    26     2    12    25    16   582   101
               9    74    45    40    35    12     6    16     8   207   518

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

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.

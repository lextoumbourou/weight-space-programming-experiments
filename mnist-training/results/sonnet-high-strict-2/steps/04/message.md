Step 3 of 15: validation loss 2.5593, accuracy 0.3107.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    42     0     0     1     0     5   900     0    42     1
               1     0   550   146     0     0    12     0   292    63     1
               2     0     0   376     8     0    38    33     1   533     1
               3     0     0    26    54     0   260    38     0   645     7
               4     0     3     0     0   110    70   270     4   462    64
               5     0     2    15     2     0   271   133     5   481     6
               6     1     0     2     0     2    25   606     0   330     1
               7     0     4    55     8    17   272    90    18   124   502
               8     0     1    75     0     0    31    10     0   891     1
               9     0     6     4     2     8   148   168     2   434   189

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 9.5504 | 0.1653
2 | 2.2641 | 0.1767
3 | 2.5593 | 0.3107

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

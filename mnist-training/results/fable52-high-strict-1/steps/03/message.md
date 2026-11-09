Step 2 of 15: validation loss 1.4921, accuracy 0.4959.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   554     0     5    18     0    20    98     0   290     6
               1     0   632     3     0    16     0     5     2   377    29
               2    22     0   228   127     2     0     9     4   544    54
               3     0     0     0   840     0    12    11     0   163     4
               4    17     2     0    22   198     3    21     2   499   219
               5     3     0     0   366     0   214   180     0   144     8
               6    26     1     3     7     0    16   526     0   381     7
               7    24     2    19    73     0    30    41   334   205   362
               8     1     0     9    30     0     1    18     2   923    25
               9    12     2     0    94     0     2    22     0   319   510

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3919 | 0.2590
2 | 1.4921 | 0.4959

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

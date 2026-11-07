Step 8 of 15: validation loss 1.4762, accuracy 0.4663.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   498     6    11     0     1     3    47     2   423     0
               1     0   795    48    26     2     1     0   169    23     0
               2    30     9   510    55     7     7     3    47   318     4
               3     1     1    26   594     3   159     1    31   212     2
               4    10    26     2     2   549     0     2    20   271   101
               5     3     7    32    64     7   244    47    13   497     1
               6    34    61    10     0    16     6   208     6   618     8
               7    10    11    24    45   145   152     3   416    66   218
               8     0    23   165    45     5    10     2   116   594    49
               9    38    21     3    10    81    45    18    48   442   255

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438
3 | 1.9209 | 0.3803
4 | 1.6809 | 0.4863
5 | 2.2016 | 0.3779
6 | 1.5165 | 0.5238
7 | 5.7134 | 0.1383
8 | 1.4762 | 0.4663

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.

Step 5 of 15: validation loss 1.0340, accuracy 0.6710.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   872    19    46     0     0    10    41     2     0     1
               1     0   974    21     0     0     0     1    63     0     5
               2    17    59   689    57    46     4    10    30    78     0
               3     3     7    29   590     0   233    31    43    83    11
               4    13   129    12     0   698     0    20    12    15    84
               5    20    16     0    34    11   481   253    11    61    28
               6   101    82    16     1    71    41   578     0    76     1
               7    48    22    31    36    28    24     0   836     0    65
               8    11   132   145     9     3     4    52    80   432   141
               9   113    51    33    24    59     9    29    60    23   560

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522
5 | 1.0340 | 0.6710

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.

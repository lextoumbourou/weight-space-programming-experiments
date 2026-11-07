Step 6 of 15: validation loss 1.0275, accuracy 0.6668.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   835    16    31     0     0     4    23     1    80     1
               1     0   962    22     0     0     1     0    73     4     2
               2    15    55   635    87    26     6     6    29   130     1
               3     3     6    24   568     0   202    14    33   170    10
               4    10   105     4     6   651     0     2     6   116    83
               5    19    13     0    27    11   482   183     6   147    27
               6    84    81    17     0    69    19   653     0    41     3
               7    45    21    35    68    27     3     1   815     5    70
               8    14    75    85    35     4    11    35    56   512   182
               9   104    46    28    35    50     3    50    38    52   555

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522
5 | 1.0340 | 0.6710
6 | 1.0275 | 0.6668

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.

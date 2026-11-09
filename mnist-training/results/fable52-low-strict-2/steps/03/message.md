Step 2 of 15: validation loss 0.9969, accuracy 0.6680.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   598    18    56     0     1     4   282     2     0    30
               1     0   969    42     0     8     0     0    27    16     2
               2    30    77   371   162    54     1     2   183    33    77
               3     4     3    18   767     1    67     8   113    42     7
               4     3    13    19     1   743     0     2    24    41   137
               5     2    14    25    80     2   552   139    42    56     3
               6    13    43    27     0    90     9   680     0    68    37
               7     4     4     4    25     5     5     6   835     2   200
               8    12   146    91    21     6    11    36   138   477    71
               9     9    12     6    11     9     7    15   180    24   688

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

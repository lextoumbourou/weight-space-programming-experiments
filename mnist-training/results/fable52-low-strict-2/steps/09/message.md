Step 8 of 15: validation loss 0.9137, accuracy 0.7124.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   833    14   105     0     0     9    29     0     0     1
               1     1   925   101     0     6     0     0     2    29     0
               2    74    64   706    58    35     0     3    25    21     4
               3    10     8   101   746     1   103     1    47    12     1
               4     8    32    95     5   781     0     2     0    14    46
               5     9     6    83    46     2   672    66     1    29     1
               6    38    33    47     0    73    49   693     0     7    27
               7    45    56    42    69    20    18    13   802     2    23
               8    31   104   203    18     8    15    39    43   515    33
               9    34    53    91    52    68    38    53   115     6   451

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909
5 | 0.9762 | 0.6769
6 | 0.8629 | 0.7278
7 | 0.8344 | 0.7409
8 | 0.9137 | 0.7124

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.

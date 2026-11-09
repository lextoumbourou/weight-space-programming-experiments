Step 10 of 15: validation loss 0.7009, accuracy 0.7977.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   816     0    65     0     0     9    34     0    66     1
               1     0   880    70     4    45     6     2    49     6     2
               2    49     2   755    71     2     3     4    27    71     6
               3     4     0    11   823     0   107     1     4    76     4
               4    19    10    38     3   667    10    43    11    37   145
               5     7     2     5    19     1   791    31    14    45     0
               6   102     4     9     0    21     5   820     0     6     0
               7    27     0    26    29     3    59     1   848    15    82
               8     1     7    57     4     2     9    21    16   850    42
               9    41     0    18    35     3    65    21    38    13   727

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882
5 | 0.8736 | 0.7192
6 | 0.9409 | 0.7196
7 | 0.8792 | 0.7403
8 | 0.7594 | 0.7718
9 | 0.7161 | 0.7895
10 | 0.7009 | 0.7977

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

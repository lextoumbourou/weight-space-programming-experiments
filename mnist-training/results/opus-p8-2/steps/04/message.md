Step 3 of 50: validation loss 1.3679, accuracy 0.6182.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   662     7    60     1     0    33   188     0    40     0
               1     1   951    80     0     5     2     1    24     0     0
               2    15    21   614    48    29    10    17     5   230     1
               3     1    12    74   532     2   162    16    22   198    11
               4     3   106    30     0   550     0    29     9    98   158
               5    10    39    33    28     3   507   206     5    80     4
               6    33    62     9     0   110     4   721     0    28     0
               7     7    33    74    22     9    44     6   591    20   284
               8    18    86   219     0     2     7    48    30   557    42
               9    37    68    29     0    19    11    50    49   201   497

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

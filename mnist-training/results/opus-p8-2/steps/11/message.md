Step 10 of 50: validation loss 1.0621, accuracy 0.6789.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   795    10   104     0     0    29    31     3    19     0
               1     0   787    97     1    11     1     0   166     1     0
               2    16     5   514   244    43     9     5    13   138     3
               3     3     1    22   786     1    87     2    37    76    15
               4     8    31    30     0   583     1     8    10   160   152
               5    10     4    14    49     7   696    99     8    25     3
               6    63    25    14     9    67     9   744     3    32     1
               7    28     6    86    36    35    48     1   702    24   124
               8     5    36   140    12     6    11    53    82   595    69
               9    66    21    36     7    19    25    14    49   137   587

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182
4 | 1.7558 | 0.5974
5 | 1.3255 | 0.5417
6 | 1.1397 | 0.6529
7 | 1.3018 | 0.5786
8 | 1.0999 | 0.6685
9 | 1.0772 | 0.6831
10 | 1.0621 | 0.6789

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

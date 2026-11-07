Step 9 of 50: validation loss 0.5545, accuracy 0.8242.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   942     0    17     0     2     0    23     0     0     7
               1     0  1005    43     0     4     0     0     2    10     0
               2    10     5   790   100    31     0    11    19    18     6
               3    10     0    40   801     2   109    23    19    16    10
               4     5    39     1     1   850     0     3     2    11    71
               5    12     9     2    32     3   721    40    20    70     6
               6    40    16     1     0    56     7   817     0     7    23
               7     7     4    22     2    12     0     2   914     1   126
               8    40    64    86    26     6    12    36    40   632    67
               9    12    13     9    13    27     0    16    90    11   770

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297
5 | 0.9636 | 0.7647
6 | 0.9087 | 0.8054
7 | 0.8223 | 0.7877
8 | 0.5529 | 0.8265
9 | 0.5545 | 0.8242

41 steps left. Reply with the complete build_weights() for step 10 in one Python code block.

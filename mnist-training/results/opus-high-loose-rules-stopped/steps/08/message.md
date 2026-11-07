Step 7 of 50: validation loss 0.8223, accuracy 0.7877.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   898     0    12     1     6     0    61     0     2    11
               1     1   927    92     0    11     3     6     5    19     0
               2    19     6   667   187    23     4    12    25    43     4
               3     6     0    29   680     3   240    26     5    35     6
               4     3    15     0     2   879     1     6     1    18    58
               5     6     5     1    41     4   678    46     4   126     4
               6     4     4     0     4    30    38   851     0    21    15
               7     3     1    47     1    65     6    18   822     2   125
               8    16    14    31    37     7    29    34    10   763    68
               9     4     0     5    15    62    23    20    46    74   712

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

43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.

Step 1 of 50: validation loss 1.4065, accuracy 0.6314.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   711    14   105     1     0    50   107     1     2     0
               1     0  1008    33     0     1     1     0    21     0     0
               2    14    50   716    86    23    10     9    15    67     0
               3     1    37    74   675     1   165     8    45    14    10
               4     1   240    41     1   493     0    26    19     7   155
               5     8   130    37    52     3   565   105     6     5     4
               6    51   154    22     1   117     8   611     0     3     0
               7     4    74    44    19     6    31     0   765     3   144
               8    27   169   285    18     5    15    55    73   304    58
               9    46   138    48     6    24    34    31   120    48   466

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314

At most 49 steps left. Reply with the complete build_weights() for step 2 in one Python code block.

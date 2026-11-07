Step 3 of 15: validation loss 1.1668, accuracy 0.6014.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   820    16    65     0     0    12    72     6     0     0
               1     0   931    24     0     0     2     1   105     0     1
               2    22    55   755    41    11     7    36    23    34     6
               3     3    11    61   492     0   222    95    89    50     7
               4    14   173    53     1   226     2    88   109     9   308
               5    29    20     1    16     3   393   386    26    21    20
               6   102    32    25     0     3     8   768     0    24     5
               7    57    21    75     6     5    32     3   874     0    17
               8    10   125   245     3     3     5   143   106   284    85
               9    96    55    64     8     0     4    76   186     1   471

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

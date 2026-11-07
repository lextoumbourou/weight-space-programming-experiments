Step 1 of 15: validation loss 1.4231, accuracy 0.5723.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   806     6    22     0     0    30    99     1    27     0
               1     0   894    37     0     0     5     7   117     4     0
               2    20    14   516    29     6     3    30     5   364     3
               3     3     2    19   405     0   189    56    13   338     5
               4    12    48     3     1   110     0   101     9   335   364
               5    22     4     0     5     0   394   360     3   119     8
               6    49    10     2     2     1     6   732     0   163     2
               7    87     9   139    36     4    48     6   663    47    51
               8     8    32    77     1     0     3   111    14   712    51
               9    72    18    14     8     0     6    86    20   246   491

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723

14 steps left. Reply with the complete build_weights() for step 2 in one Python code block.

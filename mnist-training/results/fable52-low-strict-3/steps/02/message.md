Step 1 of 15: validation loss 1.5340, accuracy 0.7380.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   640     0     3     0     0     3   323     0    22     0
               1     0   748   165     7     3     6     5    29    99     2
               2    14     0   575   103     6    20     5     1   250    16
               3     0     0     3   746     0   241     2     2    35     1
               4     2     4     6     0   836     0    38     9    69    19
               5     2     0     0    55     2   696    45     0   111     4
               6    52     1     2     0    19     1   839     0    50     3
               7     5     2    12    54    27    44    28   811    17    90
               8     5     4     4     1     2     3    25    14   945     6
               9    16     4     0     3    16    49   145   103    81   544

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5340 | 0.7380

14 steps left. Reply with the complete build_weights() for step 2 in one Python code block.

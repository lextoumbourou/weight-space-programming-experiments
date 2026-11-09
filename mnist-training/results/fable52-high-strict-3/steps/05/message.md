Step 4 of 15: validation loss 1.3566, accuracy 0.5882.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   667    11    22    15     0     0     6     0   269     1
               1     0  1016     9    22     0     0     4     3     7     3
               2    33     9   339   293     0     2     5    10   287    12
               3     6     0    16   940     0     7     2     0    56     3
               4    49    80     1    28    90     1   117     0   351   266
               5     7     7     0   555     2   173    59     1   102     9
               6    32    24     0     5     0     0   696     0   198    12
               7    71     9     7   163     0    48     0   588    74   130
               8     7    22     1    74     0     0    28     4   847    26
               9    29    26     0   168     0     1    26     5   180   526

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.

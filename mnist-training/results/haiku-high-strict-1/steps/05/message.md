Step 4 of 15: validation loss 2.2109, accuracy 0.3604.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     2    58   111    70    45   550    31   124     0
               1     0   717     2    14   324     0     0     7     0     0
               2     0     5   544   224   174    12     0    29     2     0
               3     0     1    87   500   276     9     1   156     0     0
               4     0     5     3    14   911    23     0     4    22     1
               5     0     1    37   324   218   273    28    34     0     0
               6     0    11   172   220   445    81     3     0    35     0
               7     0     6     3   314    85     4    15   655     5     3
               8     0    31    78   258   223   126     0   292     1     0
               9     0     5     0   148   687    34     2    72    13     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6085 | 0.1223
2 | 1.9985 | 0.4359
3 | 2.0168 | 0.3084
4 | 2.2109 | 0.3604

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.

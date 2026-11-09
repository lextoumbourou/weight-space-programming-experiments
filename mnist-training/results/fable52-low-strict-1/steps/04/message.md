Step 3 of 15: validation loss 0.9794, accuracy 0.7006.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   736     7    32     0     0     0   214     1     0     1
               1     0   804   131     0     1     5     2   118     0     3
               2    40    14   591   120     8     1    16    28    97    75
               3     3     0     9   807     1   112    22    11    58     7
               4    10    35    23     1   425     1    29    13   116   330
               5     4     6     4    37     0   627   204     9    19     5
               6    50    26     2     0     3     1   873     1     4     7
               7    26     4    13    11     5    16    11   815     9   180
               8     8    24   110    19     2     3    66    98   541   138
               9    22    10     9     6     0     8    23    80    16   787

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

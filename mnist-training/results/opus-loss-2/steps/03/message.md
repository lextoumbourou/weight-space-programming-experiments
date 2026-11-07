Step 2 of 50: validation loss 1.0061, accuracy 0.6721.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   710     9   182     1     0    27    37     5    19     1
               1     0   887    10     0     5     1     3   155     2     1
               2     9    24   497    56    48     2    10    20   292    32
               3     2     2     6   713     0    83     9    50   151    14
               4     5    53     8     3   382     0     8    29   102   393
               5     3     4     1    27     1   522   262    18    75     2
               6    45    24     5     0     9    21   797     1    61     4
               7     6    12    47    41    18    34     0   803    17   112
               8     3    34    24     1     1     0    85    65   686   110
               9    24    15    29    22     2     5    35    56    49   724

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721

At most 48 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 3 in one Python code block.

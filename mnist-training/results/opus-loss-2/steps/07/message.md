Step 6 of 50: validation loss 0.8788, accuracy 0.7393.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   875    11    61     0     3     9    18     0    12     2
               1     0  1010    10     0     8     5     1    18    12     0
               2     4    16   625    67   101     4    12     3   158     0
               3     0     3    39   790     3   159     3    16    13     4
               4     7    43     2     1   714     0     2     2    35   177
               5     5     5     3    33    10   585   228     5    41     0
               6    43    31     1     0    66    30   773     0    20     3
               7    11    18   151    24    36    85     1   674    10    80
               8     2    70    49     9     6    13    85    12   663   100
               9    39    34    34    18    59    10    20    20    43   684

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721
3 | 1.9548 | 0.5810
4 | 0.9710 | 0.6862
5 | 0.9076 | 0.7298
6 | 0.8788 | 0.7393

At most 44 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 7 in one Python code block.

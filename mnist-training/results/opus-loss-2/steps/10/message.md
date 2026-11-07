Step 9 of 50: validation loss 0.7760, accuracy 0.7456.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   869     9    81     0     4     9     9     4     5     1
               1     0   966     7     0     9     4     1    74     3     0
               2     5    14   667    85    95     4    12     9    99     0
               3     0     2    44   803     3   140     2    27     6     3
               4     7    35     3     1   696     0     1    13    35   192
               5     6     4     8    48    11   619   184    11    24     0
               6    65    26     1     2    85    49   720     1    16     2
               7     6     9    97    31    30    55     0   832     6    24
               8     3    49    54    17     8    13    80    52   626   107
               9    42    17    48    32    55     7    17    60    25   658

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721
3 | 1.9548 | 0.5810
4 | 0.9710 | 0.6862
5 | 0.9076 | 0.7298
6 | 0.8788 | 0.7393
7 | 0.8256 | 0.7435
8 | 0.8006 | 0.7451
9 | 0.7760 | 0.7456

At most 41 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 10 in one Python code block.

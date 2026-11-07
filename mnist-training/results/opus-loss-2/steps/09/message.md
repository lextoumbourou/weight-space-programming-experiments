Step 8 of 50: validation loss 0.8006, accuracy 0.7451.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   875     9    66     0     3     9    16     2    10     1
               1     0   997    10     0     8     5     1    35     8     0
               2     3    15   641    72   100     3    11     5   140     0
               3     0     3    37   800     3   149     1    21    12     4
               4     7    39     2     1   715     0     1     5    35   178
               5     6     6     4    48    12   593   193     7    46     0
               6    48    31     1     0    76    36   751     0    21     3
               7    11    13   121    25    34    76     0   741     9    60
               8     2    65    53    13     6    14    64    28   667    97
               9    38    30    41    23    59    10    16    31    42   671

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

At most 42 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 9 in one Python code block.

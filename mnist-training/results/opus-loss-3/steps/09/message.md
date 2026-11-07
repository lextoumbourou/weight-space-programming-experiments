Step 8 of 50: validation loss 0.9806, accuracy 0.7142.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   821    11    67     4     3    18    57     1     4     5
               1     0  1038    11     3     6     2     1     3     0     0
               2     5    32   473   405    49     3     1    11    10     1
               3     3     9     5   921     1    79     0     3     4     5
               4     0   108     0     4   812     1     9    20     0    29
               5     1    47     0   124     9   652    37    43     2     0
               6    38    53     2     1    90    30   750     0     1     2
               7     2    28    12    36     7     6     0   936     0    63
               8    35   108    77   441     3    95    26    59   154    11
               9    11    73    13    44    15    25     5   190     0   585

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259
4 | 0.9561 | 0.6843
5 | 0.9639 | 0.6853
6 | 1.0021 | 0.6652
7 | 0.9227 | 0.7348
8 | 0.9806 | 0.7142

At most 42 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 9 in one Python code block.

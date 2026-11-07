Step 4 of 50: validation loss 0.9561, accuracy 0.6843.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   771     9    39     0     2     0   114     0    36    20
               1     0   955    85     1     5     0     1    17     0     0
               2     7    33   439    68    42     0     9    36   209   147
               3     3     0    13   531     3   212    17     4   231    16
               4     1    46    11     3   577     2    20    28    90   205
               5     0     3     1   132    11   553   104    49    50    12
               6    12    43     0     0    73     4   747     0    29    59
               7     3    17    13     2    15    34     2   814     1   189
               8     6    38    22    52     1     6    42    75   707    60
               9     3    30     6     6    14    10     4   126    13   749

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259
4 | 0.9561 | 0.6843

At most 46 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 5 in one Python code block.

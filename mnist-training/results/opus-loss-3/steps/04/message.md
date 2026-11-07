Step 3 of 50: validation loss 1.1333, accuracy 0.6259.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   741    24    30     4     0     1   147     4     7    33
               1     0  1013    31     3     2     0     1    14     0     0
               2     6   105   331   231     7     0     7    62    79   162
               3     4     5     5   766     0   153    27    11    43    16
               4     0   267     5    13   246     5    19    62    10   356
               5     0    18     0   210     2   518    70    85     4     8
               6    12   150     0     0    11     4   704     0     7    79
               7     1    49     3     1     1    15     0   896     0   124
               8     7    78    14   245     0     9    50   187   361    58
               9     1    79     2    19     0     9     1   164     3   683

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259

At most 47 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 4 in one Python code block.

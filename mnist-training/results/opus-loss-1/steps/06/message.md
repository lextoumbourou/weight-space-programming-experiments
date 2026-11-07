Step 5 of 50: validation loss 1.3029, accuracy 0.6276.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   847    12   110     0     3    15     3     1     0     0
               1     0  1004    38     0     9     3     0    10     0     0
               2    11    12   614   258    67    18     1     8     1     0
               3     1     7    20   850     3   127     0    22     0     0
               4    10    98    79    22   728     9     7     3     0    27
               5    25    24     7    39    12   772     8    28     0     0
               6   118    87    18    17   121   275   331     0     0     0
               7    33     7   172    24    25    85     0   739     0     5
               8    22    90   289   370    15    37    30    75    56    25
               9   106    63   129    88    78    68     0    94     0   335

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148
2 | 1.1827 | 0.6054
3 | 1.0792 | 0.6656
4 | 1.0021 | 0.6869
5 | 1.3029 | 0.6276

At most 45 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 6 in one Python code block.

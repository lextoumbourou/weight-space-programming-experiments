Step 2 of 50: validation loss 1.1827, accuracy 0.6054.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   792     5    27     0     0     2    93     3    69     0
               1     0   706    50     0     2     3     3   300     0     0
               2    10     8   559   102     7     9    55     5   235     0
               3     2     2    18   749     0    69    73    21    84    12
               4     5    45    13     0   301     1   113    25   174   306
               5    30     4     3    12     0   369   389    20    65    23
               6    27    27     1     0     0    42   795     5    69     1
               7    36     7   177    25    11    53     5   559    27   190
               8     5    21   109     4     1     4    81    73   668    43
               9    49    23    33     5    11     0    22    49   213   556

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148
2 | 1.1827 | 0.6054

At most 48 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 3 in one Python code block.

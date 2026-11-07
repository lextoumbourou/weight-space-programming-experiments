Step 4 of 50: validation loss 0.9710, accuracy 0.6862.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   860    11    38     0     0     6    28     0    46     2
               1     0   976    32     0     5     4     2    44     1     0
               2     6    23   530    13    33     5    16     5   358     1
               3     1     3    10   710     0   166    10    23   100     7
               4     5    52     2     1   433     0     2     7   150   331
               5     3     7     1     6     1   505   249     5   136     2
               6    31    27     1     0     6    12   823     0    64     3
               7    10    23   105    15    14    41     0   563    29   290
               8     1    58    56     0     1     0    62    22   729    80
               9    24    30    35     3     3     2    26    18    87   733

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721
3 | 1.9548 | 0.5810
4 | 0.9710 | 0.6862

At most 46 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 5 in one Python code block.

Step 7 of 50: validation loss 0.9227, accuracy 0.7348.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   833     1    44     0     1     5    44     0    58     5
               1     0   929    90     7    11     9     4     7     7     0
               2    11     5   477   183    49     7     7     2   238    11
               3     4     1     7   699     1    94     1     1   217     5
               4     1    13     0     1   815     0    24    10    20    99
               5     1     7     1    92     8   652    79    18    55     2
               6    49     7     2     0    59     8   818     0    19     5
               7     5     4    32    48    12     9     1   726     6   247
               8    20    23    75   121     3    42    30    29   646    20
               9    14    12    26    19    21    17    10    66    23   753

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

At most 43 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 8 in one Python code block.

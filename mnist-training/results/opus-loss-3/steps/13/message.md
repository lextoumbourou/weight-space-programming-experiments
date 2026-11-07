Step 12 of 50: validation loss 1.0161, accuracy 0.7124.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   800    10    95     2     1    22    53     0     3     5
               1     0  1012    29     5     6     5     1     6     0     0
               2     3    17   569   292    43    16     3     5    38     4
               3     4     5    17   834     0   140     0     3    22     5
               4     1    92     3     4   725     3    26    17     2   110
               5     1    23     3   112     6   690    48    27     4     1
               6    32    32     3     0    71    39   785     0     0     5
               7     2    22    19    41     6    13     0   866     0   121
               8    27    81   141   278     3   130    58    59   215    17
               9     9    68    21    22     5    35     7   165     1   628

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
9 | 1.0125 | 0.7390
10 | 0.8095 | 0.7390
11 | 0.8708 | 0.7390
12 | 1.0161 | 0.7124

At most 38 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 13 in one Python code block.

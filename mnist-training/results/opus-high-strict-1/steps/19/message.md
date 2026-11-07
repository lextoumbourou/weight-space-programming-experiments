Step 18 of 50: validation loss 0.8502, accuracy 0.7646.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   844     9    48     0     2     5     3     0    77     3
               1     1   999    41     3    14     4     0     2     0     0
               2    52    19   687    41    74    12    14    26    53    12
               3    15     3    42   638     1   221    18     9    69    14
               4     5    27    18     0   805     2     2     6     6   112
               5    13     4     6    39     3   592    58     5   192     3
               6    61    17     2     0    16     9   850     0     6     6
               7     9     2    34    11    17     2     2   936    10    67
               8    27    53    79    41     5    22    80    49   540   113
               9    21    14    21     3    29    15     6    64    33   755

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977
4 | 1.2769 | 0.5620
5 | 1.3371 | 0.6101
6 | 1.3076 | 0.6173
7 | 2.1437 | 0.5085
8 | 1.2513 | 0.6359
9 | 1.0575 | 0.7023
10 | 1.0173 | 0.7092
11 | 1.0146 | 0.7208
12 | 0.9488 | 0.7302
13 | 0.9289 | 0.7448
14 | 0.9244 | 0.7485
15 | 0.9234 | 0.7504
16 | 0.8602 | 0.7619
17 | 0.9085 | 0.7477
18 | 0.8502 | 0.7646

At most 32 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 19 in one Python code block.

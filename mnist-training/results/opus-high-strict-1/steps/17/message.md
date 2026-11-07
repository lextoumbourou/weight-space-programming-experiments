Step 16 of 50: validation loss 0.8602, accuracy 0.7619.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   851     9    46     0     2     3     4     0    73     3
               1     1  1000    39     1    14     6     0     3     0     0
               2    53    20   685    37    74    15    15    28    52    11
               3    18     3    45   671     1   162    27    12    72    19
               4     5    27    18     0   789     3     2     7     7   125
               5    19     4     6    41     5   538    68     9   223     2
               6    63    17     2     0    14    20   840     0     5     6
               7     9     1    33    10    15     1     2   944     9    66
               8    28    52    70    32     4    49    68    49   542   115
               9    21    13    21     3    26    14     8    65    31   759

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

At most 34 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 17 in one Python code block.

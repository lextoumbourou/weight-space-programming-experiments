Step 19 of 50: validation loss 0.8487, accuracy 0.7660.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   837     9    53     0     2     5     4     0    78     3
               1     1   999    41     3    14     4     0     2     0     0
               2    42    19   700    42    72    12    13    25    53    12
               3    13     3    44   655     1   208    18     7    67    14
               4     5    27    18     0   806     2     1     6     6   112
               5    11     4     7    45     5   590    53     5   192     3
               6    57    17     2     0    19     9   849     0     7     7
               7     8     2    38    10    19     3     2   930     9    69
               8    27    52    86    49     5    23    76    46   536   109
               9    19    15    21     3    31    15     5    61    33   758

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
19 | 0.8487 | 0.7660

At most 31 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 20 in one Python code block.

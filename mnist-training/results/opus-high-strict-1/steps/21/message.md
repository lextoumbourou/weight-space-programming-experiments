Step 20 of 50: validation loss 0.9134, accuracy 0.7631.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   880     7    31     0     4     9     5     0    49     6
               1     1  1008    26     2    16     6     0     4     0     1
               2    62    24   654    62    67    24    12    28    37    20
               3    14     1    21   681     3   239    12     7    44     8
               4     5    21     9     0   805     4     3     4     3   129
               5     8     4     9    47     6   667    45     5   123     1
               6    68    19     1     0    47    29   783     0     4    16
               7     9     2    25    19    16     6     1   896     5   111
               8    28    39    70    81     3    50    97    53   459   129
               9    20    14    14     3    20    38     4    42     8   798

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
20 | 0.9134 | 0.7631

At most 30 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 21 in one Python code block.

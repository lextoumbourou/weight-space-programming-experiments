Step 25 of 50: validation loss 1.0542, accuracy 0.7213.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   921    12    52     0     0     5     0     0     0     1
               1     1   995    27     1    15     4     0    21     0     0
               2    47    28   790    23    31     8     7    38    18     0
               3    22     4    65   699     0   212     9    15     4     0
               4    11    60    50     0   841     1     2    16     0     2
               5    23     5    23    73     3   673    52    21    42     0
               6    99    24     8     0    17     7   811     0     1     0
               7    18     5    43     7    11     2     0  1004     0     0
               8    53    98   312    56    14    24    78   152   212    10
               9    98    25    63    16   130    65     8   289     0   267

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
21 | 0.8352 | 0.7727
22 | 0.8037 | 0.7563
23 | 0.8298 | 0.7737
24 | 0.8399 | 0.7689
25 | 1.0542 | 0.7213

At most 25 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 26 in one Python code block.

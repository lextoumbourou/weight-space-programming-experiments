Step 23 of 50: validation loss 0.8298, accuracy 0.7737.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   875    11    36     0     2     8     2     0    53     4
               1     1   989    26     2    22     5     0    19     0     0
               2    39    15   700    48    79    10    13    28    52     6
               3     7     2    24   708     1   211    17     5    51     4
               4     5    32    20     0   811     0     2     3     8   102
               5     9     3     6    57     3   624    50     4   158     1
               6    63    17     2     0    21     8   842     0    10     4
               7     9     4    34    16    25     1     2   896     8    95
               8    25    43    71    81    10    21    85    51   535    87
               9    20    15    11     3    46    35     4    45    25   757

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

At most 27 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 24 in one Python code block.

Step 24 of 50: validation loss 0.8399, accuracy 0.7689.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   874     7    36     0     2     9     3     0    55     5
               1     1   995    25     1    22     4     0    15     1     0
               2    38    20   685    51    80     8    13    39    51     5
               3     7     3    18   697     3   223    20    10    42     7
               4     5    31    20     0   811     0     2     2     8   104
               5     8     4     5    49     3   598    54     8   184     2
               6    63    16     2     0    22     3   847     0    10     4
               7    10     5    37     5    18     0     2   905     8   100
               8    23    53    61    89    11    20    83    55   523    91
               9    20    17    13     4    45    37     4    42    25   754

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

At most 26 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 25 in one Python code block.

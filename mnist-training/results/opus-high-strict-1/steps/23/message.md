Step 22 of 50: validation loss 0.8037, accuracy 0.7563.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   864     9    42     0     3     2     7     0    57     7
               1     0   995    27     1    21     4     0    15     1     0
               2    56    23   662    58   100     8    18    39    17     9
               3    20     3    14   723     4   221    16    11    11     7
               4    11    43    27     0   805     0     2     4     1    90
               5    28     6    13    77    11   665    50    14    49     2
               6    94    17     2     0    26     1   817     0     8     2
               7    19     5    40     5    22     0     0   918     1    80
               8    44    71   163    84    14    16    84    61   385    87
               9    45    17    10     6    57    31     3    56     7   729

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

At most 28 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 23 in one Python code block.

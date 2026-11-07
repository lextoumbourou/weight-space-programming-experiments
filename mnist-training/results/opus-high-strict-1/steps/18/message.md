Step 17 of 50: validation loss 0.9085, accuracy 0.7477.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   847    11    36     0     3     2     4     0    85     3
               1     1  1005    39     2    10     6     0     1     0     0
               2    57    34   665    33    75    12    24    30    51     9
               3    30     6    45   651     1   168    37    11    66    15
               4    13    35    23     0   770     4     3     3    10   122
               5    21     6    13    55     4   534    76     8   196     2
               6    70    30     1     0     8    16   830     0     5     7
               7    18     7    38     7    18     1     1   937     7    56
               8    29    70   101    30     5    49    81    39   489   116
               9    29    21    17     2    36    15     6    59    27   749

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

At most 33 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 18 in one Python code block.

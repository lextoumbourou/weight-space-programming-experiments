Step 25 of 50: validation loss 0.8632, accuracy 0.7298.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   853    13    65     3     0     4     8     0    44     1
               1     0   952     6     0    12     5     1    41    35    12
               2     2    10   726    70    42    10     7    29    94     0
               3     0     0    32   641     0   216     3    42    84    12
               4     7    79    12     9   769     0     4     7    25    71
               5    12     3     0    39     6   578   158    15    73    31
               6    39    64     7     9    55     4   757     0    28     4
               7    17     2    55    58    62     7     2   785     1   101
               8     8    22    60    57     5     8    26    33   632   158
               9    83    17    45    84    25     2    31    47    22   605

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522
5 | 1.0340 | 0.6710
6 | 1.0275 | 0.6668
7 | 1.0119 | 0.6788
8 | 1.0305 | 0.6521
9 | 1.1631 | 0.6279
10 | 1.0417 | 0.6767
11 | 1.0431 | 0.6827
12 | 0.9757 | 0.6870
13 | 0.9501 | 0.6891
14 | 0.9757 | 0.6901
15 | 0.9493 | 0.6901
16 | 0.9385 | 0.6967
17 | 0.9444 | 0.6945
18 | 0.9462 | 0.6999
19 | 0.9015 | 0.7112
20 | 0.8694 | 0.7234
21 | 0.8620 | 0.7257
22 | 0.8711 | 0.7286
23 | 0.8569 | 0.7327
24 | 0.8659 | 0.7267
25 | 0.8632 | 0.7298

At most 25 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 26 in one Python code block.

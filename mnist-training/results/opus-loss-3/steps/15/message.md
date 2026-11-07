Step 14 of 50: validation loss 0.7758, accuracy 0.7552.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   862     0    66     0     0     5    43     0     9     6
               1     0   878   132     6    14    10     8    12     4     0
               2    12     0   626   180    53    10     5     3    86    15
               3    13     0    30   782     1   135     1     0    62     6
               4     1     3     3     1   871     2    22     9     3    68
               5     2     0     1    77     7   708    88    16    13     3
               6    56     2     2     0    58    11   828     0     5     5
               7     4     2    41    41    11    14     0   759     2   216
               8    41    10   161   133     5    78    44    21   495    21
               9    20     5    38    21    27    28     9    64     6   743

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259
4 | 0.9561 | 0.6843
5 | 0.9639 | 0.6853
6 | 1.0021 | 0.6652
7 | 0.9227 | 0.7348
8 | 0.9806 | 0.7142
9 | 1.0125 | 0.7390
10 | 0.8095 | 0.7390
11 | 0.8708 | 0.7390
12 | 1.0161 | 0.7124
13 | 0.8041 | 0.7421
14 | 0.7758 | 0.7552

At most 36 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 15 in one Python code block.

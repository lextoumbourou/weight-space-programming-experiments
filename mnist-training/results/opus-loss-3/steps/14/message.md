Step 13 of 50: validation loss 0.8041, accuracy 0.7421.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   845     3    52     0     1     6    41     0    38     5
               1     0   923    98     5    10    10     5     8     5     0
               2    13     5   560   152    52     8     5     3   181    11
               3     7     1    27   681     1   121     1     1   185     5
               4     1    16     1     1   837     2    22    13    11    79
               5     2     6     1    76     9   684    73    23    40     1
               6    51     9     2     0    61     9   818     0    12     5
               7     4     6    41    38    11    11     0   772     4   203
               8    23    22   128   108     3    56    35    30   583    21
               9    18    13    33    16    20    28     9    92    14   718

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

At most 37 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 14 in one Python code block.

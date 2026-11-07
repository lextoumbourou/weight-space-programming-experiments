Step 18 of 50: validation loss 0.8077, accuracy 0.7442.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   875    15    47     0     4     0    28     0     9    13
               1     0   962    52     0     1     4     1    33    11     0
               2    18    16   687    76    51     6     3    25    80    28
               3     4     2    31   722     0   208     2     4    50     7
               4     3    80     6     6   776    19     4     7    29    53
               5     9     6     1   145     5   492   107     9   102    39
               6    45    67     3     0    23    22   765     0    15    27
               7    17    13    31    19     7    51     1   855     1    95
               8    16    80    91    76     2    15    14    40   614    61
               9    24    39    26    31    14    49     3    74     7   694

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541
5 | 1.0513 | 0.7082
6 | 1.0357 | 0.7054
7 | 1.6683 | 0.6427
8 | 0.9795 | 0.7212
9 | 0.9277 | 0.7288
10 | 0.9119 | 0.7315
11 | 0.8657 | 0.7409
12 | 0.8425 | 0.7394
13 | 0.8340 | 0.7436
14 | 0.8773 | 0.7451
15 | 0.8129 | 0.7451
16 | 13.3371 | 0.1117
17 | 0.8871 | 0.7342
18 | 0.8077 | 0.7442

At most 32 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 19 in one Python code block.

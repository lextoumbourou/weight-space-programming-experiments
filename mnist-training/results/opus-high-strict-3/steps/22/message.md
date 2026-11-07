Step 21 of 50: validation loss 0.7994, accuracy 0.7507.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   859    18    50     0     6     2    27     0    15    14
               1     0   975    51     0     1     8     2    19     8     0
               2    15    16   706    87    38     9     2    25    65    27
               3     3     2    25   704     0   205     2     6    76     7
               4     2    80     5     8   754    19     5     6    38    66
               5     7     5     5   138     5   512    89     6   113    35
               6    32    58     4     0    26    24   784     0    15    24
               7    18    13    25    21     7    41     1   865     5    94
               8    14    74    85    63     2    19    14    32   649    57
               9    23    39    13    30    17    48     2    69    21   699

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
19 | 0.8010 | 0.7508
20 | 0.8976 | 0.7271
21 | 0.7994 | 0.7507

At most 29 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 22 in one Python code block.

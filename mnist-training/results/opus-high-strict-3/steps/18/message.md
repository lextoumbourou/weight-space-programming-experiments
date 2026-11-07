Step 17 of 50: validation loss 0.8871, accuracy 0.7342.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   850    15    23     0     1     1    46     0    38    17
               1     0   983    57     0     0    12     2     3     7     0
               2    17    15   609    95    19     2     6    23   165    39
               3     6     1    17   809     1   125     6     2    55     8
               4     2    80     2    10   618    11    16     5    56   183
               5     5     6     0   159     3   383   133     3   165    58
               6    17    49     1     0     5     8   819     0    21    47
               7    17    15    29    33     4    19     2   805     8   158
               8    16    68    36    78     0     7    18    11   698    77
               9    17    36     6    60     1    21     4    35    13   768

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

At most 33 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 18 in one Python code block.

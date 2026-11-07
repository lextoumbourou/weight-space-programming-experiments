Step 19 of 50: validation loss 0.8010, accuracy 0.7508.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   867    18    46     0     6     1    28     0    11    14
               1     0   977    46     0     1     7     2    23     8     0
               2    17    16   701    82    38     8     3    23    73    29
               3     3     3    24   708     0   212     2     6    65     7
               4     2    81     4     8   756    19     4     7    39    63
               5     8     6     4   138     4   513    91     5   109    37
               6    36    65     3     0    22    24   777     0    14    26
               7    18    13    24    21     6    45     1   862     5    95
               8    14    76    78    67     2    18    15    34   649    56
               9    23    40    17    27    14    48     4    72    18   698

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

At most 31 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 20 in one Python code block.

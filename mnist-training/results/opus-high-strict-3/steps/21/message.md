Step 20 of 50: validation loss 0.8976, accuracy 0.7271.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   836    21    52     0     5     2    32     1    28    14
               1     0  1004    41     0     1     8     2     3     5     0
               2    17    29   698    82    39     8     2    26    66    23
               3     2     5    18   810     0   140     2     0    47     6
               4     2   132     4    41   661    15     8     5    41    74
               5     7    14     8   227     4   463    84     3    73    32
               6    19    86     3     1    28    20   782     0    11    17
               7    18    30    23    52     5    32     0   836     4    90
               8    13   140    87   103     1    16    15    21   559    54
               9    22    58     8   156     7    36     2    42     8   622

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

At most 30 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 21 in one Python code block.

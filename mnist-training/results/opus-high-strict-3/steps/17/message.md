Step 16 of 50: validation loss 13.3371, accuracy 0.1117.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    58     0     0     0    27     3     0     0   903     0
               1     0     0     0     0     0     0     0     0  1064     0
               2     0     0     0     0     1     0     0     0   989     0
               3     0     0     0     0     0     0     0     0  1030     0
               4     0     0     0     0    49     0     0     0   933     1
               5     0     0     0     0     3     0     0     0   912     0
               6     0     0     0     0    63     0     0     0   902     2
               7     0     0     0     0     0     0     0     2  1088     0
               8     0     0     0     0     1     0     0     0  1008     0
               9     0     0     0     0     2     0     0     0   959     0

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

At most 34 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 17 in one Python code block.

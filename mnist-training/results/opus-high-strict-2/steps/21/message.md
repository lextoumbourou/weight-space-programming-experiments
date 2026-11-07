Step 20 of 50: validation loss 0.8694, accuracy 0.7234.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   872    13    49     2     0     2     8     0    44     1
               1     0   969    10     0     7     3     1    29    37     8
               2     7     9   680   100    54    13    10    28    89     0
               3     1     0    25   684     1   212     2    26    75     4
               4     5    74     9    26   736     0     2     5    21   105
               5    13     4     0    31    10   592   144    13    80    28
               6    28    65     6     4   123     1   710     0    25     5
               7    24     3    55   112    26     5     3   792     2    68
               8     8    27    73    57     4     7    28    24   600   181
               9    87    20    31   125    13     4    33    33    16   599

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

At most 30 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 21 in one Python code block.

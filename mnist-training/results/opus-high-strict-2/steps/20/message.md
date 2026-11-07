Step 19 of 50: validation loss 0.9015, accuracy 0.7112.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   873    13    46     0     0     6     8     0    44     1
               1     0   972     9     0     6     2     1    27    38     9
               2     8     9   663   111    47    24    10    28    90     0
               3     3     0    21   550     1   327     3    22    98     5
               4     6    76     7    39   726     0     3     4    20   102
               5    15     6     0     9    10   609   143    11    81    31
               6    29    66     6     2   123     1   709     0    26     5
               7    27     3    52   108    26    14     3   781     2    74
               8     9    27    63    48     5    10    29    19   607   192
               9    92    22    28    88    13    18    33    29    16   622

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

At most 31 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 20 in one Python code block.

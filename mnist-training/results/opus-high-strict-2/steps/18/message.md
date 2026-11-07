Step 17 of 50: validation loss 0.9444, accuracy 0.6945.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   863    20    53     1     0     5    10     0    38     1
               1     0   979    16     0     7     3     1    39     4    15
               2     8    18   684    75    50    18    11    38    88     0
               3     1     1    28   623     0   251     2    26    94     4
               4     7    71     5    22   715     0     1     4    55   103
               5    14     4     1    18    10   610   102    14   117    25
               6    30    71     5     6   152     3   667     0    28     5
               7    29     4    45   113    27     9     2   774     6    81
               8    12    52    97    65     4    16    31    42   442   248
               9    91    25    33   108    11     6    26    25    48   588

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

At most 33 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 18 in one Python code block.

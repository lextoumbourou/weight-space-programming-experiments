Step 18 of 50: validation loss 0.9462, accuracy 0.6999.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   877    21    46     0     0     2     8     0    36     1
               1     0   987    17     0     5    22     1    27     1     4
               2     9    17   684    95    42    15    11    28    89     0
               3     2     1    28   574     0   296     2    26    94     7
               4     8    76     6    34   687     1     1     4    57   109
               5    14     9     1     7     8   638   122    11    86    19
               6    32    73     6     1   115    13   700     0    22     5
               7    29     5    52   113    23     7     2   778     3    78
               8     8    57    93    48     5    21    31    38   455   253
               9    95    26    23    88    11    15    20    23    41   619

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

At most 32 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 19 in one Python code block.

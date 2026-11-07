Step 16 of 50: validation loss 0.9385, accuracy 0.6967.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   830    23    61     2     0     9    10     0    55     1
               1     0  1003    17     0     5     4     2    17     4    12
               2     7    19   692    69    42    19    11    29   102     0
               3     2     2    30   607     0   232     2    27   123     5
               4     6    94     7    25   677     0     1     4    70    99
               5    13    12     1    22     8   600   115    13   108    23
               6    25    77     5     7   113     1   711     0    25     3
               7    26     5    55    89    23     6     2   801     4    79
               8    11    64   101    60     4    13    32    38   460   226
               9    84    34    35    95    10     4    24    27    62   586

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

At most 34 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 17 in one Python code block.

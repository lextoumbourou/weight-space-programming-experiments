Step 10 of 15: validation loss 1.0417, accuracy 0.6767.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   846    16    34     1     0     7     3     0    83     1
               1     0   975    24     0     1     4     0    55     5     0
               2     8    36   648   112    25    15    10    23   113     0
               3     2     3    29   572     0   261     2    21   132     8
               4     9    91     6     9   642     1     1     2   129    93
               5    16    11     0     6     6   612    70     5   174    15
               6    44    89     7     0    98     7   653     0    68     1
               7    37    20    59   107    24     7     1   740    16    79
               8    15    62   102    41     3    12    24    29   525   196
               9   102    39    37    50     7    17    15    15   125   554

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

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

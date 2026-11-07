Step 6 of 15: validation loss 1.2805, accuracy 0.5933.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   790    12    17     0     0     0    75     8    42    47
               1     0  1013    45     1     0     3     0     2     0     0
               2    16    52   581    69    26    15    27    10   112    82
               3     2    49    11   600     1   204    89    36    31     7
               4     2   110    11     0   638    20     0    46    31   125
               5    10   133     6    90     1   429    88    97    20    41
               6    33   123    12    11    89    77   464     0    32   126
               7    11    85    10    14    14    18     3   810     1   124
               8     0   204   201   120     0    48    13   156   227    40
               9     6   132     3     4   120    69     1   230    15   381

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.1586 | 0.4753
2 | 1.4530 | 0.4972
3 | 1.2907 | 0.5670
4 | 1.3876 | 0.4982
5 | 1.2362 | 0.5778
6 | 1.2805 | 0.5933

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.

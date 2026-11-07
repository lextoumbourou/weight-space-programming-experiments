Step 9 of 15: validation loss 1.7466, accuracy 0.4891.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   885     8    67     0     2     3     8     0    17     1
               1     0   837    84     1     0     9     0   133     0     0
               2    50    15   727    74    15    69    13     1    25     1
               3     7     9    64   656     0   269     0     9    14     2
               4   156   109   212    45    55   261    15    12     7   111
               5    10    34    93    99     0   661     6     9     3     0
               6   166    59   121    21     8   207   381     0     3     1
               7    28    46   216   178     0   185     0   397     2    38
               8    29    72   422    61     1   206    23    17   159    19
               9   111    98   129    65     2   363     3    44    13   133

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 7.1815 | 0.2094
2 | 2.1968 | 0.2092
3 | 1.9429 | 0.3361
4 | 1.7848 | 0.3318
5 | 1.7825 | 0.3806
6 | 1.7746 | 0.3360
7 | 2.9444 | 0.2186
8 | 3.9520 | 0.4274
9 | 1.7466 | 0.4891

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.

Step 5 of 15: validation loss 0.8282, accuracy 0.7383.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   818     2    75     1     0    20    70     0     5     0
               1     0   941    48     3    43     0     1    14     8     6
               2    24     1   500   337    16     1     3    10    55    43
               3     4     0     5   929     1    71     0     6     9     5
               4    32    13    30    23   708     1    57     7    33    79
               5     9     2     4   112     2   685    56     4    39     2
               6   109    16     1     0    44     7   764     0    25     1
               7    21     0    15    84    18    41     0   650     2   259
               8    33    20    36    41     4    14    27    24   782    28
               9    53     9    15   108    10    80    34    40     6   606

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9981 | 0.6911
2 | 1.2553 | 0.6304
3 | 0.8910 | 0.7126
4 | 10.2460 | 0.0684
5 | 0.8282 | 0.7383

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
